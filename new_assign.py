import json
import pickle

flag = True
user_input = True
new_list = []
while user_input: 
    print('Type 1: Write the File')
    print('Type 2: Output the File')
    print('Type q: Quit program')
    user_choice = input('Your choice: ')
    if user_choice == '1': 
        with open('assign.p', mode = 'wb') as f:
            while flag: 
                user2_input = input('Type anything: ')
                new_list.append(user2_input)
                decision = input('Are you done: (y/n): ')
                if decision.lower() == 'y':
                    f.write(pickle.dumps(new_list))
                    flag = False
    elif user_choice == '2':
        with open('assign.p', mode ='rb') as f:
            print(pickle.loads(f.read()))
    else:
        user_input = False