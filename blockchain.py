from utility.hash_util import hash_block
from utility.verification import Verification
from utility.printable import Printable

import functools
from transaction import Transaction
from block import Block

MINING_REWARD = 10.0


class Blockchain(Printable):
    def __init__(self, chain, open_transactions, peer_nodes, node_id):
        self.chain = chain
        self.open_transactions = open_transactions
        self.peer_nodes = peer_nodes
        self.node_id = node_id
 
    def get_open_transactions(self):
        return self.open_transactions

    def get_last_blockchain_value(self):
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def proof_of_work(self):
        last_block = self.get_last_blockchain_value()
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.is_valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self, participant):
        if not participant:
            return 0.00

        sender_sent_amounts = [[transaction.amount for transaction in block.transactions
                                if transaction.sender == participant] for block in self.chain]
        sender_open_transactions_amount = [transaction.amount
                                           for transaction in self.open_transactions if transaction.sender == participant]
        amount_sent = functools.reduce(lambda transaction_sum, transaction_amount: transaction_sum + sum(
            transaction_amount) if len(transaction_amount) > 0 else transaction_sum, sender_sent_amounts, 0)

        amount_sent = amount_sent + functools.reduce(
            lambda transaction_sum, transaction_amount: transaction_sum + transaction_amount, sender_open_transactions_amount, 0)

        sender_received_amounts = [[transaction.amount for transaction in block.transactions
                                    if transaction.recipient == participant] for block in self.chain]
        amount_received = functools.reduce(lambda transaction_sum, transaction_amount: transaction_sum + sum(
            transaction_amount) if len(transaction_amount) > 0 else transaction_sum, sender_received_amounts, 0)

        return amount_received - amount_sent

    def add_transaction(self, recipient, amount, sender, signature):
        transaction = Transaction(sender, recipient, amount, signature)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            return True
        return False

    def mine_block(self, recipient):
        if recipient == None:
            return False

        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()

        reward_transaction = Transaction('MINING', recipient, MINING_REWARD, '')

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        mined_block = Block(hashed_block, len(
            self.chain), copied_transactions, proof)
        self.chain.append(mined_block)
        self.open_transactions = []
        return mined_block

    def add_peer_node(self, node):
        self.peer_nodes.add(node)
    
    def remove_peer_node(self, node):
        self.peer_nodes.discard(node)
    
    def get_all_nodes(self):
        return list(self.peer_nodes)