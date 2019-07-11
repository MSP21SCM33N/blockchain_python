import functools
import hashlib as hl
import json
import requests
from collections import OrderedDict#Used to ensure that the transactions remain ordered
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = [] #unhandled transactions
        self.public_key = public_key
        self.__peer_nodes = set() # Creating a set of peer nodes 
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data() # Execute whenever the blockchain is loaded 

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
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f: #Reads the data in binary
                #file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain'] #Goes up to but not including the new line character
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain #The setter kicks in 
                open_transactions = json.loads(file_content[1][:-1]) #Reads everything up until the new character (line break)
                updated_txs = []
                for tx in open_transactions: # To load open transactions as ordered dictionaries
                    updated_tx =  Transaction(tx['sender'], tx['recipient'], tx['signature'],tx['amount'])
                    updated_txs.append(updated_tx)
                self.__open_transactions = updated_txs 
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError): 
            pass
        finally: # Runs code regardless of an error thrown
            print('Cleanup')
                

    def save_data(self): # Save open transactions and blockchain to a file
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]] #Stores a snapshot as binary data of our blockchian
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx)) #Will Fail because it is a lit of open transaction objects
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
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
        
                                            
    def balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
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
        

    def add_transaction(self, sender, recipient, signature, amount=1, is_receiving=False):
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
       # if self.public_key == None: #Public key is stored in the hosting node
        #    return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature':signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined. Needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False
    #add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

    def mine_block(self): # Adding our open transactions into a new block
        if self.public_key == None: #Public key is stored in the hosting node
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block) # Did a one line for loop that returns the previous block
        proof = self.proof_of_work()
        """ reward_transaction = {
            'sender' : 'MINING',
            'recipient' : owner, 
            'amount': MINING_REWARD
        } """
        reward_transaction = Transaction('MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]     # Added copied transactions in that case that our new block failed to add to our block chain. A reward should not be given when if the append block has failed. 
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        
        copied_transactions.append(reward_transaction)
        new_block = Block(len(self.__chain), hashed_block, copied_transactions, proof) #new block object
            # Our way of knowing linking our new block to the previous(i.e )
        self.__chain.append(new_block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = new_block.__dict__.copy()
            converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Transaction declined. Needs resolving')
                    if response.status_code == 409:
                        self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue

        return new_block

    def add_block(self, block):
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
        proof_is_valid = Verification.verify_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'],block['timestamp'])
        self.__chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']: #for incoming transactions in block['transactions]
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json() # Getting json data from an incoming response Json returns back a dictionary
                node_chain =[Block(block['index'], block['previous_hash'], [Transaction(
                    tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']],
                                    block['proof'], block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node): 

        """Function adds a node to the peer node set
        Arguments:#
            :node: Node url which should be added. 
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Function removes a node to the peer node set
        Arguments:#
            :node: Node url which should be removed. 
        """
        self.__peer_nodes.discard(node)
        self.save_data()
        
    def get_peer_nodes(self):
        """
        Returns a list of all connected peer nodes
        """
        return list(self.__peer_nodes)





    


