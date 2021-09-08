MINING_REWARD = 10.0

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Jona'
participants = {owner}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, amount, sender=owner):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(recipient)


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:
        return True
    print('Insufficient balance: ' + str(sender_balance))
    return False


def get_balance(participant):
    sender_sent_amounts = [[transaction['amount'] for transaction in block['transactions'] if transaction['sender'] == participant] for block in blockchain]
    sender_open_transactions_amount = [transaction['amount'] for transaction in open_transactions if transaction['sender'] == participant]
    amount_sent = 0
    for transaction_amount in sender_sent_amounts:
        if len(transaction_amount) > 0:
            amount_sent += transaction_amount[0]
    for amount in sender_open_transactions_amount:
        amount_sent += amount
    
    sender_received_amounts = [[transaction['amount'] for transaction in block['transactions'] if transaction['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for transaction_amount in sender_received_amounts:
        if len(transaction_amount) > 0:
            amount_received += transaction_amount[0]
    
    return amount_received - amount_sent


def get_transaction_data():
    recipient = input('Enter the recipient of the amount: ')
    amount = float(input('Your transaction amount please: '))
    return recipient, amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    copied_transactions = open_transactions[:];
    copied_transactions.append({
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    })
    blockchain.append({
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    })
    print(blockchain)
    return True



def get_user_input():
    return input('Your choice please: ')


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if (index == 0):
            continue
        elif (block['previous_hash'] != hash_block(blockchain[index - 1])):
            return False
    return True


def print_blockchain_elements():
    for block in blockchain:
        print('Outputting block')
        print(block)

    print('-' * 20)

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_user_input = True

while waiting_for_user_input:
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
        print(open_transactions)
    elif (user_input == '2'):
        if mine_block():
            open_transactions = []
    elif (user_input == '3'):
        print_blockchain_elements()
    elif (user_input == '4'):
        print(participants)
    elif (user_input == '5'):
        if verify_transactions:
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

    if not verify_chain():
        print_blockchain_elements()
        print('Invalid chain!')
        break

print('Done!')
