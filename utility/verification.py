from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet

class Verification:
    @staticmethod # Made verify_proof a static method since we're only dependent on the arguments given
    def verify_proof(transactions, last_hash, proof): 
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        gues_hash = hash_string_256(guess)
        print(gues_hash)
        return gues_hash[0:2] == '00'

    @classmethod # Accesses the verify_proof function however, the whole class is a help class and does not need an instance
    def verify_chain(cls, blockchain): # If the first block of the new blockchain does not equal the whole value of the previous blockchain, the blockchain is invalid. 
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index -1]):
                return False
            if not cls.verify_proof(block.transactions[:-1], block.previous_hash, block.proof): # Call self on a method because it is in the class
                print('Proof of work is invalid')
                return False
        return True #Compares the previous block to the previous hash

    @staticmethod
    def verify_transaction(transaction, balance, checkfunds =True):
        if checkfunds:
            sender_balance = balance()
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, balance):
        return all([cls.verify_transaction(tx, balance, False) for tx in open_transactions])