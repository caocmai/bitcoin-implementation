
from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4


node_identifier = str(uuid4()).replace('-','')

app = Flask(__name__)

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