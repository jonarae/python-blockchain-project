from time import time
from transaction import Transaction
from utility.printable import Printable


class Block(Printable):
    def __init__(self, previous_hash='', index='', transactions='', proof='', timestamp=1, dict=None):
        if dict is None:
            self.previous_hash = previous_hash
            self.index = index
            self.transactions = transactions
            self.timestamp = timestamp
            self.proof = proof
        else:
            self.previous_hash = dict['previous_hash']
            self.index = dict['index']
            self.timestamp = dict['timestamp']
            self.proof = dict['proof']
            
            self.transactions = []
            for transaction in dict['transactions']:
                self.transactions.append(Transaction(dict=transaction))

    def to_order_dict(self):
        order_dict = self.__dict__.copy()
        order_dict['transactions'] = []
        for transaction in self.transactions:
            order_dict['transactions'].append(transaction.to_order_dict())

        return order_dict
