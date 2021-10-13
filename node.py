from hashlib import blake2b
from flask import Flask, json, jsonify, request
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

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance(wallet.public_key)
    response = {
        'funds': balance
    }
    return jsonify(response), 200


@app.route('/wallet', methods=['POST'])
def create_and_save_wallet():
    if wallet.create_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(wallet.public_key)
        }
        wallet.save_keys()
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating of wallet and keys failed!'
        }
        return jsonify(response), 500


@app.route('/wallet', methods=['GET'])
def load_wallet():
    if wallet.load_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(wallet.public_key)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Loading of wallet and keys failed!'
        }
        return jsonify(response), 500


@app.route('/mine', methods=['POST'])
def mine_block():
    mined_block = blockchain.mine_block(wallet.public_key)
    if mined_block:
        BlockchainFile.save_data(blockchain)
        mined_block_dict = mined_block.__dict__.copy()
        mined_block_dict['transactions'] = [transaction.__dict__.copy()
                                for transaction in mined_block.transactions]

        response = {
            'message': 'Successfully added a new block!',
            'block': mined_block_dict,
            'funds': blockchain.get_balance(wallet.public_key)
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding new block failed!',
            'wallet_up': wallet.public_key != None
        }
        return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def get_chain():
    blockchain_snapshot = blockchain.chain
    blockchain_snapshot = [block.__dict__.copy()
                           for block in blockchain_snapshot]
    for block in blockchain_snapshot:
        block['transactions'] = [transaction.__dict__.copy()
                                 for transaction in block['transactions']]
    return jsonify(blockchain_snapshot), 200


@app.route ('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400
    
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400

    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing'
        }
        return jsonify(response), 400

    recipient = values['recipient']
    amount = values['amount']
    
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    is_success = blockchain.add_transaction(recipient, amount, wallet.public_key, signature)

    if is_success:
        BlockchainFile.save_data(blockchain)
        response = {
            'funds': blockchain.get_balance(wallet.public_key),
            'message': 'Successfully added transaction',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            }
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Adding of transaction failed'
        }
        return jsonify(response), 500
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
