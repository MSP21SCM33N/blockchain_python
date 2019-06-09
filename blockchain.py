import functools
import hashlib as hl
import json
from collections import OrderedDict#Used to ensure that the transactions remain ordered
from hash_util import hash_block, hash_string_256
import pickle

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = 'Max'
participants = {'Max'} #Set

def load_data(): 
    global blockchain
    global open_transactions
    try: 
        with open('blockchain.txt', mode='r') as f: #Reads the data in binary
            #file_content = pickle.loads(f.read())
            file_content = f.readlines()
            # blockchain = file_content['chain'] #Goes up to but not including the new line character
            # open_transactions = file_content['ot']
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                    'previous_hash': block['previous_hash'],
                    'index' : block['index'],
                    'proof': block['proof'],
                    'transactions': [OrderedDict(
                        [('sender', tx['sender']), ('recipient', tx['recipient']), 
                            ('amount', tx['amount'])]) for tx in block['transactions']] 
                    
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_txs = []
            for tx in open_transactions: # To load open transactions as ordered dictionaries
                updated_tx =  OrderedDict(
                        [('sender', tx['sender']), ('recipient', tx['recipient']), 
                            ('amount', tx['amount'])]) 
                updated_txs.append(updated_tx)
            open_transactions = updated_txs 
    except IOError: 
        print('File not found') #Initializes our blockchain when we do not have data from a file
        genesis_block = {
        'previous_hash' : '',
        'index' : 0, 
        'transactions' : [],
        'proof' : 100
        }
        blockchain = [genesis_block]
        open_transactions = []
    finally: # Runs code regardless of an error thrown
        print('Cleanup')
            

load_data()

def save_data(): # Save open transactions and blockchain to a file
    try:
        with open('blockchain.txt', mode='w') as f: #Stores a snapshot as binary data of our blockchian
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            # save_data = {
            #     'chain': blockchain, 
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving Failed')




     
def verify_proof(transactions, last_hash, proof): 
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    gues_hash = hash_string_256(guess)
    print(gues_hash)
    return gues_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not verify_proof(open_transactions, last_hash, proof): #Will keep executing until the verify_proof return true
        proof += 1

    return proof
    
                                           
def balance(participant):
    tx_sender = [[tx['amount']for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] 
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = 0
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0) # Returns the total amount of coins sent
    amount_received = 0
    tx_recipient = [[tx['amount']for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0) # Returns the amount of coins received

    return amount_received - amount_sent

def get_transcation_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount #Returns a tuple

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def get_last_item():
    if (len(blockchain) < 1):
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = balance(transaction['sender'])
    return sender_balance >= transaction['amount']
    

def add_transaction(recipient, sender=owner, amount=1.0):
    """
        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: Amount of coins sent
    """ # default argument
    """ transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    } """ # Initializing a dictionary
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False

#add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

def mine_block(): # Adding our open transactions into a new block
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block) # Did a one line for loop that returns the previous block
    proof = proof_of_work()
    """ reward_transaction = {
        'sender' : 'MINING',
        'recipient' : owner, 
        'amount': MINING_REWARD
    } """
    reward_transaction =  OrderedDict(
        [('sender', 'MINING'),('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:] # Added copied transactions in that case that our new block failed to add to our block chain. A reward should not be given when if the append block has failed. 
    copied_transactions.append(reward_transaction)
    new_block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transactions,
        'proof': proof
        } # Our way of knowing linking our new block to the previous(i.e )
    blockchain.append(new_block)
    return True

def verify_chain(): # If the first block of the new blockchain does not equal the whole value of the previous blockchain, the blockchain is invalid. 
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index -1]):
            return False
        if not verify_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True #Compares the previous block to the previous hash

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

def print_func():
    for block in blockchain:
        print('Outputing block')
        print(block)
        print('-' * 50)

waiting_for_input = True
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check Transaction Validity')
    print('q: To quit the program')
    print('h: Manipulate the blockchain')
    user_input = get_user_choice()

    if (user_input == '1'):
        tx_data = get_transcation_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount): #Allows us to skip the middle argument(Sender)
            print('Added Transaction!')
        else:
            print('Transaction Failed!')

        
    elif(user_input == '2'):
        if mine_block():
            open_transactions = []
            save_data()
    elif (user_input == '3'):
        print_func()
    elif(user_input == '4'):
        print(participants)
    elif(user_input == '5'):
        if verify_transactions():
            print('All transactions are valid! ')
        else:
            print('There are invalid transactions! ')
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0, 
                'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
            }
    elif(user_input == 'q'):
        waiting_for_input = False
    else:
        print("Invalid input, choose either 1 or 2 ")
    print('Choice registered')

    if not verify_chain(): #If verify does not equal true, the blockchain is invalid
        print_func()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f} '.format('Max', balance('Max')))
        
print('Done')

    


