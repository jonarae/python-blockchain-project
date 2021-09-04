blockchain = []

def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def add_value(transaction_amount, last_transaction=[1]):
    if (last_transaction == None):
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])

def get_transaction_amount():
    return float(input('Your transaction amount please: '))

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

waiting_for_user_input = True

while waiting_for_user_input:
    print('Please choose');
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')

    user_input = get_user_input()
    
    if (user_input == '1'):
        tx_amount = get_transaction_amount()
        add_value(tx_amount, get_last_blockchain_value())
    elif (user_input == '2'):
        for block in blockchain:
            print('Outputting block')
            print(block)
    elif (user_input == 'q'):
        waiting_for_user_input = False
    elif (user_input == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = 2
    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain():
        print('Invalid chain!')
        break

print('Done!')
