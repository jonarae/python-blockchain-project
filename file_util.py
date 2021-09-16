import pickle

def save_data(blockchain, open_transactions):
    with open('blockchain.txt', mode='wb') as f:
        f.write(pickle.dumps({
            'blockchain': blockchain,
            'open_transactions': open_transactions
        }))

def load_data():
    with open('blockchain.txt', mode='rb') as f:
        return pickle.loads(f.read())
        