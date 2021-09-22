from time import time
from utility.printable import Printable


class Block(Printable):
    def __init__(self, previous_hash, index, transactions, proof, timestamp=time()):
        self.previous_hash = previous_hash
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.proof = proof

    def to_order_dict(self):
        return self.__dict__.copy()
