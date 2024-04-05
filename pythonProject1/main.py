# Lib / Dependencies
# Flask --> Web Framework, json, jsonify
# UUID --> UUID1 (not recommended because its not secure) & UUID4
# hashlib --> sha256
# time
# sys
# urlparse --> localhost:8080/blockchain
# requests

import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask,redirect,url_for,render_template
from flask.globals import request
from flask.json import jsonify


# First block --> Genesis block
class Blockchain(object):
    difficulty_level = "0"

    def __init__(self):
        self.chain = []
        self.current_transaction = []
        # For the genesis block, the previous block hash is set to '0'
        genesis_block = {
            'index': 0,
            'transactions': [],
            'timestamp': time(),
            'nonce': 0,
            'Previous_block_hash': '0'  # Previous block hash set to '0'
        }
        self.chain.append(genesis_block)

    def Block_Hash(self, block):
        # json.dumps convert the Python Object into JSON String
        blockEncoder = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha512(blockEncoder).hexdigest()

    # Proof of Work vs Proof of Stake
    def PoW(self, index, Previous_block_hash, transactions):
        nonce = 0

        while self.validate_Proof(index, Previous_block_hash,
                                  transactions, nonce) is False:
            nonce += 1
            print(nonce)
        print(nonce)
        return nonce

    def validate_Proof(self, index, Previous_block_hash, transactions, nonce):
        data = f'{index},{Previous_block_hash},{transactions},{nonce}'.encode()
        hash_data = hashlib.sha512(data).hexdigest()
        return hash_data[:len(self.difficulty_level)] == self.difficulty_level

    def append_block(self, nonce, Previous_block_hash):
        block = {
            'index': len(self.chain),
            'transactions': self.current_transaction,
            'timestamp': time(),
            'nonce': nonce,
            'Previous_block_hash': Previous_block_hash
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        self.current_transaction.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]


# Flask , #routes
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', "")
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

# routes --> /admissions /scholarship
@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine_block():
    start = time()
    blockchain.add_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    last_block_hash = blockchain.Block_Hash(blockchain.last_block)
    index = len(blockchain.chain)
    nonce = blockchain.PoW(index, last_block_hash, blockchain.current_transaction)
    block = blockchain.append_block(nonce, last_block_hash)
    response = {
        'message': "new block has been added (mined)",
        'index': block['index'],
        'hash_of_previous_block': block['Previous_block_hash'],
        'nonce': block['nonce'],
        'transaction': block['transactions']
    }
    end = time()
    print(end-start)
    return jsonify(response), 200


@app.route('/transaction/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']  # corrected 'receipient' to 'recipient'
    if not all(k in values for k in required_fields):
        return 'Missing Fields', 400
    index = blockchain.add_transaction(
        values['sender'],
        values['recipient'],  # corrected 'receipient' to 'recipient'
        values['amount']
    )
    response = {'message': f'Transaction will be added to the block {index}'}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)