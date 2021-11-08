from flask import helpers
from flask.json import jsonify
from utility.hash_util import hash_block
from utility.verification import Verification
from utility.printable import Printable

import functools
import requests
import pickle
from transaction import Transaction
from block import Block

MINING_REWARD = 10.0


class Blockchain(Printable):
    def __init__(self, chain, open_transactions, peer_nodes, node_id):
        self.chain = chain
        self.open_transactions = open_transactions
        self.peer_nodes = peer_nodes
        self.node_id = node_id

    def to_order_dict(self):
        blockchain_dict = self.__dict__.copy()
        blockchain_dict['peer_nodes'] = list(self.peer_nodes)
        
        blockchain_dict['chain'] = []
        blockchain_dict['open_transactions'] = []

        for block in self.chain:
            blockchain_dict['chain'].append(block.to_order_dict())
        for transaction in self.open_transactions:
            blockchain_dict['open_transactions'].append(transaction.to_order_dict())
            

        return blockchain_dict
 
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

    def add_transaction(self, recipient, amount, sender, timestamp, signature, from_broadcast=False):
        transaction = Transaction(sender, recipient, amount, timestamp, signature)

        if from_broadcast:
            check_funds = False
        else:
            check_funds = True

        if Verification.verify_transaction(transaction, self.get_balance, check_funds):
            self.open_transactions.append(transaction)
            self.broadcast_transaction(transaction)
            return True
        return False
    
    def broadcast_transaction(self, transaction):
        for node_id in self.peer_nodes:
            requests.post(f'http://{node_id}/transaction', json={
                'recipient': transaction.recipient,
                'amount': transaction.amount,
                'sender': transaction.sender,
                'timestamp': transaction.timestamp,
                'signature': transaction.signature,
                'from_broadcast': True
            })
 
 
    def mine_block(self, recipient):
        if recipient == None:
            return False

        last_block = self.get_last_blockchain_value()
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        
        reward_transaction = Transaction('MINING', recipient, MINING_REWARD, '')

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        mined_block = Block(hashed_block, len(self.chain), copied_transactions, proof)
        self.chain.append(mined_block)
        self.open_transactions = []
        self.broadcast_mined_block(mined_block)
        return mined_block


    def broadcast_mined_block(self, mined_block):
        for node_id in self.peer_nodes:
            requests.post(
                f'http://{node_id}/block',
                json={
                    'block': mined_block.to_order_dict()
                }
            )
    
    def add_block(self, mined_block):
        block = Block(dict=mined_block)

        last_block = self.get_last_blockchain_value()
        hashed_block = hash_block(last_block)

        is_previous_hash_valid = block.previous_hash == hashed_block
        is_proof_valid = Verification.is_valid_proof(self.open_transactions, hashed_block, block.proof)
        is_index_valid = block.index == len(self.chain)

        if is_previous_hash_valid and is_index_valid and is_proof_valid:
            self.chain.append(block)
            self.update_open_transactions(block)
            return True
        else: 
            if block.index > len(self.chain):
                self.resolve()
                return True
            return False

    def resolve(self):
        valid_chain = self.chain
        longest_chain_length = len(self.chain)
        to_replace_chain = False

        for node_id in self.peer_nodes:
            response = requests.get(f'http://{node_id}/chain')
            peer_blockchain_dict = response.json()['blockchain']

            peer_blockchain = []
            for block_dict in peer_blockchain_dict:
                peer_blockchain.append(Block(dict=block_dict))

            is_peer_blockchain_longer = len(peer_blockchain) > longest_chain_length

            if is_peer_blockchain_longer and Verification.verify_chain(peer_blockchain):
                valid_chain = peer_blockchain
                to_replace_chain = True
        
        if to_replace_chain:
            self.chain = valid_chain
            self.open_transactions = []

        return True

    def update_open_transactions(self, block):
        for transaction in block.transactions:
            for open_transaction in self.open_transactions:
                if transaction.signature == open_transaction.signature:
                    self.open_transactions.remove(open_transaction)


    def add_peer_node(self, node):
        self.peer_nodes.add(node)
    
    def remove_peer_node(self, node):
        self.peer_nodes.discard(node)
    
    def get_all_nodes(self):
        return list(self.peer_nodes)