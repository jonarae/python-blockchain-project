import functools
import hashlib
from hash_util import hash_block


def print_blockchain_elements(blockchain):
    print('-' * 20)
    for block in blockchain:
        print('Outputting block')
        print(block)

    print('-' * 20)


def get_last_blockchain_value(blockchain):
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def proof_of_work(blockchain, open_transactions):
    last_block = get_last_blockchain_value(blockchain)
    last_hash = hash_block(last_block)
    proof = 0
    while not is_valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def is_valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    if guess_hash[0:2] == '00':
        print('-' * 50)
        print(f'guess: {guess}')
        print(f'guess_hash: {guess_hash}')
        print('-' * 50)
        return True

    return False


def get_balance(participant, blockchain, open_transactions):
    sender_sent_amounts = [[transaction['amount'] for transaction in block['transactions']
                            if transaction['sender'] == participant] for block in blockchain]
    sender_open_transactions_amount = [transaction['amount']
                                       for transaction in open_transactions if transaction['sender'] == participant]
    amount_sent = functools.reduce(lambda transaction_sum, transaction_amount: transaction_sum + sum(
        transaction_amount) if len(transaction_amount) > 0 else transaction_sum, sender_sent_amounts, 0)

    amount_sent = amount_sent + functools.reduce(
        lambda transaction_sum, transaction_amount: transaction_sum + transaction_amount, sender_open_transactions_amount, 0)

    sender_received_amounts = [[transaction['amount'] for transaction in block['transactions']
                                if transaction['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda transaction_sum, transaction_amount: transaction_sum + sum(
        transaction_amount) if len(transaction_amount) > 0 else transaction_sum, sender_received_amounts, 0)

    return amount_received - amount_sent


def verify_transaction(transaction, blockchain, open_transactions):
    sender_balance = get_balance(
        transaction['sender'], blockchain, open_transactions)
    if sender_balance >= transaction['amount']:
        return True
    print('Insufficient balance!ß')
    return False


def verify_transactions(open_transactions):
    return all([verify_transaction(tx) for tx in open_transactions])


def verify_chain(blockchain):
    for (index, block) in enumerate(blockchain):
        if (index == 0):
            continue
        elif (block['previous_hash'] != hash_block(blockchain[index - 1])):
            return False

        block_excluding_reward_transaction = block['transactions'][:-1]
        if not is_valid_proof(block_excluding_reward_transaction, block['previous_hash'], block['proof']):
            return False
    return True
