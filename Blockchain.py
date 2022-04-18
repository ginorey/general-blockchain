
"""

First Blockchain

@author: gino

"""

# Importing Libaries

# Each block has their own time stamp, which is the exact date/time
# the block is mined 
import datetime 

# Use to hash the blocks, hash functions
import hashlib

# To encode blocks before hashing them
import json

# Create an object of Flask Class
# Also to return the messages we recieve from Postman
from flask import Flask, jsonify




# Building the Blockchain 

class Blockchain:
    
    def __init__(self):
        # The chain itself
        self.chain = []
        # Genesis Block
        self.create_block(proof = 1, previous_hash = '0')
    
    # Function inorder to to add a new block onto the chain
    # after solving the proof of work
    def create_block(self, proof, previous_hash):
        # Each block is defined by four keys
        # Index, Timestamp, Proof, Previous Hash
        block = {        'index': len(self.chain) + 1,  
                     'timestamp': str(datetime.datetime.now()),
                         'proof': proof,
                 'previous_hash': previous_hash             }
        self.chain.append(block)
        return block

    # Retrieving last block of the chain    
    def get_previous_block(self):
        return self.chain[-1]
    
    # Proof of work is the number they need to find 
    # to solve the problem
    # Challenging to Solve / Easy to Verify
    def proof_of_work(self, previous_proof):
        # We will look for the proof by increasing new_proof+1 re
        new_proof = 1
        # Once, we find the right proof, we will change check_proof 
        check_proof = False
        # We will iterate inorder to find the correct proof
        while check_proof is False:
            # Hexadecimal String
            # Non-symmetrical (not - new + previous = new)
            # Encode will add a B before the String (Ex. b'5' instead of '5')
            # Example Output = <sha256 HASH object @ 0x181656df08>
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # We will check if the four first characters of hash_operation are 0's
            # Then the miner wins! 
            # Check_proof will be set to True & the new proof will be returned
            if hash_operation [:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
            
    # Returns the cryptographic hash of our function
    def hash(self, block):
        # We are encoding our block so it can be accepted by SHA256
        # We use .dumps functions to make our block dictionary a string
        # Soft_keys is set to true inorder to  sort our dictionary by the keys
        # We use .encode inorder to get the B expected at the beginning of the string 
        encoded_block = json.dumps(block, sort_keys = True).encode()
        # Hexdigest inorder to get the hexidecimal format
        return hashlib.sha256(encoded_block).hexdigest()
    
    # We will iterate through each block in our chain.
    # Check if our blockchain is valid
    # Check that the previous hash of each block is valid to previous one
    # Check if our proof_of_work is valid under our function
    def is_chain_valid(self, chain):
        # First Block of the chain
        previous_block = chain[0]
        block_index = 1
        # Won't stop the loop until the index reaches the end of the chain
        while block_index < len(chain):
            # First block
            block = chain[block_index]
            # Checking if the hash of our previous block != our current block
            # If it isn't we return False because the chain isn't valid
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # Checking if the proof of the previous block and the current block
            # Are valid under our hash operation
            previous_proof = previous_block['proof']
            proof = block['proof']
            # We change which proofs we find the operation for
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation [:4] != '0000':
                return False
            
            # Updating our pointers inorder to iterate through the next blocks
            previous_block = block
            block_index += 1
        return True
            
#-----------------------------------------------------------------------------#           
            
 
# Mining the Chain
    
# Creating the Flask Based Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating the Blockchain
blockchain = Blockchain()
    
# Mining a New Block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    # Mine a block
    # Solve the Proof of Work Problem, Based on the previous proof
    # Once we get it, we will get the other keys
    # Index, Timestamp, Previous Hash
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    # Will contain all the information of the block & also a message
    response = {      'message': 'Congratz! You just mined a block!',
                       'index' : block['index'],
                    'timestamp': block['timestamp'],
                        'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the Full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain':  blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#-----------------------------------------------------------------------------#           

# Running the app

# We are going to make the blockchain public on my own local network
app.run(host = '0.0.0.0', port = 8000)
