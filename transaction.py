from utility.printable import Printable

class Transaction(Printable):
    def __init__(self, sender, recipient, amount, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_order_dict(self):
        return self.__dict__.copy()