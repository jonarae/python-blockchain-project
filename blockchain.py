genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Jona'


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, amount, sender=owner):
    open_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    })


def get_transaction_data():
    recipient = input('Enter the recipient of the amount: ')
    amount = float(input('Your transaction amount please: '))
    return recipient, amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = '-'.join([str(last_block[key]) for key in last_block])
    blockchain.append({
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    })
    print(blockchain)


def get_user_input():
    return input('Your choice please: ')


def verify_chain():
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] != blockchain[block_index-1]:
            return False
    else:
        return True


def print_blockchain_elements():
    for block in blockchain:
        print('Outputting block')
        print(block)


waiting_for_user_input = True

while waiting_for_user_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')

    user_input = get_user_input()

    if (user_input == '1'):
        transaction_data = get_transaction_data()
        recipient, amount = transaction_data
        add_transaction(recipient, amount)
        print(open_transactions)
    elif (user_input == '2'):
        mine_block()
    elif (user_input == '3'):
        print_blockchain_elements()
    elif (user_input == 'q'):
        waiting_for_user_input = False
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = 2
    else:
        print('Input was invalid, please pick a value from the list!')

    # if not verify_chain():
    #     print_blockchain_elements()
    #     print('Invalid chain!')
    #     break

print('Done!')
