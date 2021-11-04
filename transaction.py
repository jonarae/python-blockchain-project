from utility.printable import Printable

class Transaction(Printable):
    def __init__(self, sender='', recipient='', amount='', signature='', dict=None):
        if dict is None:
            self.sender = sender
            self.recipient = recipient
            self.amount = amount
            self.signature = signature
        else:
            self.sender = dict['sender']
            self.recipient = dict['recipient']
            self.amount = dict['amount']
            self.signature = dict['signature']

    def to_order_dict(self):
        return self.__dict__.copy()