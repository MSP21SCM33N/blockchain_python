from uuid import uuid4 #This package helps generate a new uniform unique id
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:
    def __init__(self): # Each instance will have a local blockchain 
        #self.wallet = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input

    def get_transcation_value(self):
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount please: '))
        return tx_recipient, tx_amount #Returns a tuple

    def print_func(self):
        for block in self.blockchain.chain: # We need to access the Chain Property of our blockchain object
            print('Outputing block')
            print(block)
        else:
            print('-' * 50)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check Transaction Validity')
            print('5: Create Wallet') #Generates the public and private keys and stores it in a file
            print('6: Load Wallet') #Load the file and keys
            print('7: Save Keys')
            print('q: To quit the program')
            user_input = self.get_user_choice()

            if (user_input == '1'):
                tx_data = self.get_transcation_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount): #Allows us to skip the middle argument(Sender)
                    print('Added Transaction!')
                else:
                    print('Transaction Failed!')
                print(self.blockchain.get_open_transactions())

            elif(user_input == '2'): 
                if not self.blockchain.mine_block():
                    print('Mining failed. No wallet found?')
            elif (user_input == '3'):
                self.print_func()
            elif(user_input == '4'):
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.balance):
                    print('All transactions are valid! ')
                else:
                    print('There are invalid transactions! ')
            elif (user_input == '5'):
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif (user_input == '6'):
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif (user_input == '7'):
                self.wallet.save_keys()
            elif(user_input == 'q'):
                waiting_for_input = False
            else:
                print("Invalid input, choose either 1 or 2 ")
            print('Choice registered')
            if not Verification.verify_chain(self.blockchain.chain): #If verify does not equal true, the blockchain is invalid
                self.print_func()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f} '.format(self.wallet.public_key, self.blockchain.balance()))
        print('Done')

if __name__ == '__main__': #In this context, we only want to run the UI if we're running this file directly, so we should use name to only generate the file for that reason
    node = Node() 
    node.listen_for_input()

#qprint(__name__) #Main file we called to execute