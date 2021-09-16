from collections import OrderedDict
from hash_util import hash_block
from input_util import get_transaction_data, get_user_input
from blockchain_util import proof_of_work, get_balance, verify_transaction, verify_transactions, verify_chain, print_blockchain_elements
from file_util import save_data, load_data

MINING_REWARD = 10.0

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Jona'
participants = {owner}

blockchain_data = load_data()
blockchain = blockchain_data['blockchain']
open_transactions = blockchain_data['open_transactions']


def add_transaction(recipient, amount, sender=owner):
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])

    if verify_transaction(transaction, blockchain, open_transactions):
        open_transactions.append(transaction)
        participants.add(recipient)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work(blockchain, open_transactions)

    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    blockchain.append({
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    })
    return True


waiting_for_user_input = True

while waiting_for_user_input:
    print('-' * 20)
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine new block')
    print('3: Output the blockchain blocks')
    print('4: Print Participants')
    print('5: Verify Open Transactions')
    print('h: Manipulate the chain')
    print('q: Quit')

    user_input = get_user_input()

    if (user_input == '1'):
        transaction_data = get_transaction_data()
        recipient, amount = transaction_data
        add_transaction(recipient, amount)
        save_data(blockchain, open_transactions)
    elif (user_input == '2'):
        if mine_block():
            open_transactions = []
            save_data(blockchain, open_transactions)
    elif (user_input == '3'):
        print_blockchain_elements(blockchain)
    elif (user_input == '4'):
        print(participants)
    elif (user_input == '5'):
        if verify_transactions(open_transactions):
            print('All transactions are valid')
        else:
            print('There are invalid transactions!')
    elif (user_input == 'q'):
        waiting_for_user_input = False
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '1234sdfd', 'index': 0, 'transactions': [
                {'sender': 'Angelie', 'recipient': 'Jona', 'amount': 100000}]}
    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain(blockchain):
        print('Invalid chain!')
        print_blockchain_elements()
        break

    current_balance = get_balance(owner, blockchain, open_transactions)
    print(f'Balance of {owner}: {current_balance:10.2f}')

print('Done!')
