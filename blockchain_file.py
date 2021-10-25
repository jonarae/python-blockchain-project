from blockchain import Blockchain
from block import Block
import pickle


class BlockchainFile:
    @staticmethod
    def save_data(blockchain):
        try:
            with open('blockchain.txt', mode='wb') as f:
                f.write(pickle.dumps({
                    'blockchain': blockchain.chain,
                    'open_transactions': blockchain.open_transactions,
                    'peer_nodes': list(blockchain.peer_nodes)
                }))
        except IOError:
            print('File was not saved!')

    @staticmethod
    def load_data():
        try:
            with open('blockchain.txt', mode='rb') as f:
                blockchain_data = pickle.loads(f.read())
                return Blockchain(blockchain_data['blockchain'], blockchain_data['open_transactions'], set(blockchain_data['peer_nodes']))

        except IOError:
            genesis_block = Block('', 0, [], 100)
            blockchain = [genesis_block]
            open_transactions = []
            peer_nodes = set()
            return Blockchain(blockchain, open_transactions, peer_nodes)
