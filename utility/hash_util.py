import hashlib
import json


def hash_block(block):
    converted_block = block.to_order_dict()
    converted_transactions = [transaction.to_order_dict()
                              for transaction in converted_block['transactions']]
    converted_block['transactions'] = converted_transactions
    return hashlib.sha256(json.dumps(converted_block, sort_keys=True).encode()).hexdigest()
