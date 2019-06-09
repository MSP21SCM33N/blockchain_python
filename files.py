with open('demo.txt', mode='r') as f: # Creates a text file if not yet already created, w enables overwriting info in the file
#f.write('Hello from python \n')
    line = f.readline()
    while line:
        print(line)
        line = f.readline()
print('Done')
