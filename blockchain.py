import hashlib
import json
from time import time
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')

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


blockchain = Blockchain()

# mine or verify new transaction, this must be called to validiate transaction to add to blockchain
# otherwise will not add to the chain because not yet verified
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # rewarding miner
    blockchain.new_transaction(
        sender="0", 
        recipient=node_identifier, 
        amount=1
        )

    # creating the new block and adding to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'The new block has been forged(added)',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print("value\n\n\n\n\n\n\n", values)
    required = ['sender', 'recipient', 'amount']

    # validing that all three fields are present
    if not all(k in values for k in required):
        return 'Missing values', 400

    # adding to blockchain and return the index of that chain
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction is scheduled to be added to Block No. {index}'}
    return jsonify(response), 201

# getting the blockchain
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)