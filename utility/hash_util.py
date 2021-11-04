import hashlib
import json


def hash_block(block):
    converted_block = block.to_order_dict()
    return hashlib.sha256(json.dumps(converted_block, sort_keys=True).encode()).hexdigest()
