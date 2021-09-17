import pickle
from typing import IO

def save_data(blockchain, open_transactions):
    try:
        with open('blockchain.txt', mode='wb') as f:
            f.write(pickle.dumps({
                'blockchain': blockchain,
                'open_transactions': open_transactions
            }))
    except IOError:
        print('File was not saved!')

def load_data():
    try:
        with open('blockchain.txt', mode='rb') as f:
            return pickle.loads(f.read())
    except IOError:
        genesis_block = {
            'previous_hash': '',
            'index': 0,
            'transactions': [],
            'proof': 100
        }
        blockchain = [genesis_block]
        open_transactions = []
        return {
            'blockchain': blockchain,
            'open_transactions': open_transactions
        }
        