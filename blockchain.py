import hashlib
import json
from time import time




class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="My Custom blockchain", proof=100)

    def new_block(self, proof, previous_hash=None):
        '''Create a new block'''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.pending_transactions = []
        self.chain.append(block)
        return block

    @property
    def last_block(self):
        '''Get last block'''
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        '''Create new transaction'''
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        ''' Getting the hash '''
        string_object = json.dumps(block, sort_keys=True)

        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)

        hex_hash = raw_hash.hexdigest()

        return hex_hash
    
    def proof_of_work(self, last_proof):
        ''' Doing proof of work '''
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        '''This is to validate'''
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

# blockchain = Blockchain()
# t1 = blockchain.new_transaction("Satoshi", "Mike", "5 BTC")
# t2 = blockchain.new_transaction("Mike", "Satoshi", "1 BTC")
# t3 = blockchain.new_transaction("Satoshi", "Hal", '5 BTC')
# blockchain.new_block(12345)

# t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
# t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
# t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
# blockchain.new_block(6789)

# print("Genesis block: ", blockchain.chain)



