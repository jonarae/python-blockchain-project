import argparse
from hashlib import blake2b
from flask import Flask, json, jsonify, request, send_from_directory
from flask_cors import CORS
from wallet import Wallet
from blockchain_file import BlockchainFile

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')

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

    if 'from_broadcast' in values and values['from_broadcast'] is True:
        sender = values['sender']
        signature = values['signature']
        from_broadcast = True
    else:
        sender = wallet.public_key
        signature = wallet.sign_transaction(sender, recipient, amount)
        from_broadcast = False

    if signature:
        for transaction in blockchain.open_transactions:
            if signature == transaction.signature:
                response = {
                    'message': 'Transaction is already in blockchain'
                }
                return jsonify(response), 200

    if wallet.public_key == None:
        response = {
            'message': 'No wallet setup'
        }
        return jsonify(response), 400

    is_success = blockchain.add_transaction(recipient, amount, sender, signature, from_broadcast)

    if is_success:
        BlockchainFile.save_data(blockchain)
        response = {
            'funds': blockchain.get_balance(sender),
            'message': 'Successfully added transaction',
            'transaction': {
                'sender': sender,
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


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    open_transactions = blockchain.get_open_transactions()
    open_transactions_dict = [transaction.__dict__.copy() for transaction in open_transactions]
    return jsonify(open_transactions_dict), 200


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 401
    if not 'node' in values:
        response = {
            'message': 'No node data found.'
        }
        return jsonify(response), 401
    
    node = values['node']
    blockchain.add_peer_node(node)
    BlockchainFile.save_data(blockchain)

    response = {
        'message': 'Node added successfully',
        'all_nodes': blockchain.get_all_nodes()
    }
    return jsonify(response), 200

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'No node found.'
        }
        return jsonify(response), 400
    
    blockchain.remove_peer_node(node_url)
    BlockchainFile.save_data(blockchain)

    response = {
        'message': 'Removed node successfully.',
        'all_nodes': blockchain.get_all_nodes()
    }
    return jsonify(response), 200
    

@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_all_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    node_id = args.port

    wallet = Wallet(node_id)
    blockchain = BlockchainFile.load_data(node_id)
    app.run(host='0.0.0.0', port=node_id)
