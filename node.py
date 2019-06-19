from uuid import uuid4 #This package helps generate a new uniform unique id
from blockchain import Blockchain
from verification import Verification

class Node:
    def __init__(self): # Each instance will have a local blockchain 
        #self.id = str(uuid4())
        self.id = 'MAX'
        self.blockchain = Blockchain(self.id)

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
            print('q: To quit the program')
            user_input = self.get_user_choice()

            if (user_input == '1'):
                tx_data = self.get_transcation_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount): #Allows us to skip the middle argument(Sender)
                    print('Added Transaction!')
                else:
                    print('Transaction Failed!')
                print(self.blockchain.get_open_transactions)

            elif(user_input == '2'):
                self.blockchain.mine_block()
            elif (user_input == '3'):
                self.print_func()
            elif(user_input == '4'):
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.balance):
                    print('All transactions are valid! ')
                else:
                    print('There are invalid transactions! ')
            elif(user_input == 'q'):
                waiting_for_input = False
            else:
                print("Invalid input, choose either 1 or 2 ")
            print('Choice registered')
            if not Verification.verify_chain(self.blockchain.chain): #If verify does not equal true, the blockchain is invalid
                self.print_func()
                print('Invalid blockchain!')
                break
            print('Balance of {}: {:6.2f} '.format(self.id, self.blockchain.balance()))
        print('Done')

node = Node()
node.listen_for_input()