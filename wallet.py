from Crypto.PublicKey import RSA #Public key crypto algorithm
from Crypto.Signature import pkcs1_15#algorithm that generates signatures
from Crypto.Hash import SHA256
import Crypto.Random
import binascii #Converts binary to ascii

class Wallet:
    def __init__(self): # The reason we set the keys in the constructor to None is because each time we may not want to set new keys
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys() #Unpacks the tuple from generate keys
        self.private_key = private_key
        self.public_key = public_key
        

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                    return True
            except(IOError, IndexError): #Catches the error if the file is there but has nothing in it
                print('Saving wallet failed...')
                return False

    def load_keys(self): #Loads keys already existing
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines() #List of keys from the file
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
                return True
        except(IOError, IndexError):
            print('Loading wallet failed')
            return False


    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read) # Generates a new private key
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')) #Der is binary encoding. 
        #Gives a string representation of our key.
        #hexlify puts our string in hexadecimal format and 

    def sign_transaction(self, sender, recipient, amount):
        signer = pkcs1_15.new(RSA.import_key(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8')) #enocdes our string to a binary string
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii') #converts the binary signature to string format

    @staticmethod
    def verify_transaction(transaction): #using public keys as addresses in our network
        try:
            public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
            verifier = pkcs1_15.new(public_key)
            h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
            if (verifier.verify(h, binascii.unhexlify(transaction.signature))) == None:
                return True
        except ValueError:
            return False