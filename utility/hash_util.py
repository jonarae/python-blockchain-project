import hashlib
import json


def hash_block(block):
    converted_block = block.to_order_dict()
    block_json_string = json.dumps(converted_block, sort_keys=True)

    encoded_block = block_json_string.encode()
    hashed_block = hashlib.sha256(encoded_block)
    hashed_block_hex = hashed_block.hexdigest()
    
    return hashed_block_hex
