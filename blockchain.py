
blockchain = []

def get_transcation_value():
    user_input = float(input('Your transaction amount please: '))
    return user_input

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def get_last_item():
    if (len(blockchain) < 1):
        return None
    return blockchain[-1]

def add_transaction (trans_amount, last_transc=[1]): # default argument
    if (last_transc == None):
        last_transc = [1]
    blockchain.append([last_transc,trans_amount]) #[] types casts a list
    print(blockchain)

#add_transaction (last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

def verify_chain(): # If the first block of the new blockchain does not equal the whole value of the previous blockchain, the blockchain is invalid. 
    block_index = 0
    is_valid = True
    for blocks in blockchain:
        if block_index == 0:
            block_index+=1
            continue # will skip the default  transaction and go to another iteration starting at next blocks in sequence
        elif blocks[0] == blockchain[block_index -1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index+=1
    return is_valid

def print_func():
    for block in blockchain:
        print('Outputing block')
        print(block)

while True:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('q: To quit the program')
    print('h: Manipulate the blockchain')
    user_input = get_user_choice()

    if (user_input == '1'):
        tx_amount = get_transcation_value()
        add_transaction (tx_amount, get_last_item())
    elif (user_input == '2'):
        print_func()
        print(blockchain[0])
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif(user_input == 'q'):
        break
    else:
        print("Invalid input, choose either 1 or 2 ")
    print('Choice registered')

    if not verify_chain(): #If verify does not equal true, the blockchain is invalid
        print('Invalid blockchain!')
        break
        
print('Done')

    


