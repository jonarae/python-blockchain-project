import hashlib
from utility.hash_util import hash_block
from wallet import Wallet


class Verification:
    @staticmethod
    def is_valid_proof(transactions, last_hash, proof):
        guess = (str(transactions) + str(last_hash) + str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[0:2] == '00'

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        sender_balance = get_balance(transaction.sender)
        if check_funds and sender_balance < transaction.amount:
            print('Insufficient balance!')
            return False
        elif not Wallet.verify_transaction(transaction):
            print('Transaction was manipulated!')
            return False
        else:
            return True

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        check_funds = False
        return all([cls.verify_transaction(tx, get_balance, check_funds) for tx in open_transactions])

    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain.chain):
            if (index == 0):
                continue
            elif (block.previous_hash != hash_block(blockchain.chain[index - 1])):
                return False

            block_excluding_reward_transaction = block.transactions[:-1]
            if not cls.is_valid_proof(block_excluding_reward_transaction, block.previous_hash, block.proof):
                return False
        return True
