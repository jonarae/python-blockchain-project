from flask import Flask, jsonify
from flask_cors import CORS
from wallet import Wallet
from blockchain_file import BlockchainFile

app = Flask(__name__)
wallet = Wallet()
blockchain = BlockchainFile.load_data()
CORS(app)

@app.route('/', methods=['GET'])
def get_ui():
    return 'This works!'

@app.route('/chain', methods=['GET'])
def get_chain():
    blockchain_snapshot = blockchain.chain
    blockchain_snapshot = [block.__dict__.copy() for block in blockchain_snapshot]
    for block in blockchain_snapshot:
        block['transactions'] = [transaction.__dict__.copy() for transaction in block['transactions']]
    return jsonify(blockchain_snapshot), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
