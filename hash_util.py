import json
import hashlib as hl

def hash_string_256(string): # Created a utility function 
    return hl.sha256(string).hexdigest()

def hash_block(block):
    """
    sha256: is an algorithm that creates a 64 bit hash
            Ensures same input will lead to same hash 
            The hash is returned as a byte hash
    json: 
        encodes complex data objects into strings

    encode:
        encodes the string to utf-8 to be used in the sha256

    hextdigest:
        converts the byte hash into a normal string hash

    Solved an issue with the dictionary in that if something in memory changes, the hash generated from the 
    dictionary block can actually change since a dictionary is an unordered data structure. 
    Sorting the keys ensures that this issue doesn't occur    
     """               
    return hash_string_256((json.dumps(block, sort_keys=True).encode()))