
blockchain = []

def get_transcation_value():
    user_input = float(input('Your transaction amount please: '))
    return user_input

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def get_last_item():
    return blockchain[-1]

def add_value(trans_amount, last_transc=[1]): # default argument
    
    blockchain.append([last_transc,trans_amount]) #[] types casts a list
    print(blockchain)

tx_amount = float(input("Please enter transaction amount: ")) #Type cast our input to a float
add_value(tx_amount)
#add_value(last_transc = get_last_item(), trans_amount = 1.0) keyword arguments

def print_func():
    for block in blockchain:
        print('Outputing block')
        print(block)

while True:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    user_input = get_user_choice()

    if (user_input == '1'):
        tx_amount = get_transcation_value()
        add_value(tx_amount, get_last_item())
    elif (user_input == '2'):
        print_func()
    else:
        print("Invalid input, choose either 1 or 2 ")
        

    


