MINING_REWARD = 10
genesis_block = {
    'previous hash' : '',
    'index' : 0, 
    'transactions' : []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Max'
participants = {'Max'} #Set

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def balance(participant):
    tx_sender = [[tx['amount']for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    amount_sent = 0
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant] 
    tx_sender.append(open_tx_sender)
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount']for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
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
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    } # Initializing a dictionary
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

#add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

def mine_block(): # Adding our open transactions into a new block
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block) # Did a one line for loop that returns the previous block
    reward_transaction = {
        'sender' : 'MINING',
        'recipient' : owner, 
        'amount': MINING_REWARD
    }
    copied_transactions = open_transactions[:] # Added copied transactions in that case that our new block failed to add to our block chain. A reward should not be given when if the append block has failed. 
    copied_transactions.append(reward_transaction)
    new_block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transactions
        } # Our way of knowing linking our new block to the previous(i.e )
    blockchain.append(new_block)

    return True

def verify_chain(): # If the first block of the new blockchain does not equal the whole value of the previous blockchain, the blockchain is invalid. 
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index -1]):
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
        print(open_transactions)

        
    elif(user_input == '2'):
        if mine_block():
            open_transactions = []
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
    print(balance('Max'))
        
print('Done')

    


