from blockchain import Blockchain
from block import Block
import pickle


class BlockchainFile:
    @staticmethod
    def save_data(blockchain):
        try:
            node_id = blockchain.node_id
            with open(f'blockchain-{node_id}.txt', mode='wb') as f:
                f.write(pickle.dumps({
                    'blockchain': blockchain.chain,
                    'open_transactions': blockchain.open_transactions,
                    'peer_nodes': list(blockchain.peer_nodes)
                }))
        except IOError:
            print('File was not saved!')

    @staticmethod
    def load_data(node_id):
        try:
            with open(f'blockchain-{node_id}.txt', mode='rb') as f:
                blockchain_data = pickle.loads(f.read())
                return Blockchain(blockchain_data['blockchain'], blockchain_data['open_transactions'], set(blockchain_data['peer_nodes']), node_id)

        except IOError:
            genesis_block = Block(index=0, transactions=[],
                                  proof=100, timestamp=1)
            blockchain = [genesis_block]
            open_transactions = []
            peer_nodes = set()
            return Blockchain(blockchain, open_transactions, peer_nodes, node_id)
