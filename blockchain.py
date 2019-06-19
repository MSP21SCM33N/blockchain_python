import functools
import hashlib as hl
import json
from collections import OrderedDict#Used to ensure that the transactions remain ordered
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = [] #unhandled transactions
        self.load_data() # Execute whenever the blockchain is loaded 
        self.hosting_node_id = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]# returns a copy of the chain so if you edit it, doesn't affect the original

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self): 
        try: 
            with open('blockchain.txt', mode='r') as f: #Reads the data in binary
                #file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain'] #Goes up to but not including the new line character
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain #The setter kicks in 
                open_transactions = json.loads(file_content[1])
                updated_txs = []
                for tx in open_transactions: # To load open transactions as ordered dictionaries
                    updated_tx =  Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_txs.append(updated_tx)
                self.__open_transactions = updated_txs 
        except (IOError, IndexError): 
            pass
        finally: # Runs code regardless of an error thrown
            print('Cleanup')
                

    def save_data(self): # Save open transactions and blockchain to a file
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]] #Stores a snapshot as binary data of our blockchian
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx)) #Will Fail because it is a lit of open transaction objects
                # save_data = {
                #     'chain': blockchain, 
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving Failed')


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.verify_proof(self.__open_transactions, last_hash, proof): #Will keep executing until the verify_proof return true
            proof += 1

        return proof
        
                                            
    def balance(self):
        participant = self.hosting_node_id
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant] 
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = 0
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0) # Returns the total amount of coins sent
        amount_received = 0
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0) # Returns the amount of coins received

        return amount_received - amount_sent





    def get_last_item(self):
        if (len(self.__chain) < 1):
            return None
        return self.__chain[-1]
        

    def add_transaction(self, recipient, sender,amount=1.0):
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
        transaction = Transaction(sender, recipient, amount)
        
        if Verification.verify_transaction(transaction, self.balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    #add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

    def mine_block(self): # Adding our open transactions into a new block
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block) # Did a one line for loop that returns the previous block
        proof = self.proof_of_work()
        """ reward_transaction = {
            'sender' : 'MINING',
            'recipient' : owner, 
            'amount': MINING_REWARD
        } """
        reward_transaction = Transaction('MINING', self.hosting_node_id, MINING_REWARD)
        copied_transactions = self.__open_transactions[:] # Added copied transactions in that case that our new block failed to add to our block chain. A reward should not be given when if the append block has failed. 
        copied_transactions.append(reward_transaction)
        new_block = Block(len(self.__chain), hashed_block, copied_transactions, proof) #new block object
            # Our way of knowing linking our new block to the previous(i.e )
        self.__chain.append(new_block)
        self.__open_transactions = []
        self.save_data()
        return True






    


