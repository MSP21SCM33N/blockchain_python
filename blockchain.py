
blockchain = []
open_transactions = []
owner = 'Max'

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

    open_transactions.append(transaction)
    return

#add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

def mine_block():
    pass

def verify_chain(): # If the first block of the new blockchain does not equal the whole value of the previous blockchain, the blockchain is invalid. 
    #block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue # will skip the default  transaction and go to another iteration starting at next blocks in sequence
        elif blockchain[block_index][0] == blockchain[block_index -1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid

def print_func():
    for block in blockchain:
        print('Outputing block')
        print(block)

waiting_for_input = True
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('q: To quit the program')
    print('h: Manipulate the blockchain')
    user_input = get_user_choice()

    if (user_input == '1'):
        tx_data = get_transcation_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount) #Allows us to skip the middle argument(Sender)
        print(open_transactions)
    elif (user_input == '2'):
        print_func()
        print(blockchain[0])
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif(user_input == 'q'):
        waiting_for_input = False
    else:
        print("Invalid input, choose either 1 or 2 ")
    print('Choice registered')

    if not verify_chain(): #If verify does not equal true, the blockchain is invalid
        print('Invalid blockchain!')
        break
        
print('Done')

    


