def unlimited_arguments(*args): # pointer to the arguments
    print(args)
    for argument in args:
        print(argument)

unlimited_arguments([1,2,3,4,5]) # passing a list returns one argument because all the data is reference by one pointer
unlimited_arguments(*[1,2,3,4,5])