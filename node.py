from blockchain_file import BlockchainFile
from utility.verification import Verification


class Node:
    def __init__(self):
        self.id = 'JONA'
        self.blockchain = BlockchainFile.load_data()

    def get_transaction_data(self):
        recipient = input('Enter the recipient of the amount: ')
        amount = float(input('Your transaction amount please: '))
        return recipient, amount

    def get_user_input(self):
        return input('Your choice please: ')

    def print_blockchain_elements(self):
        print('-' * 20)
        for block in self.blockchain.chain:
            print('Outputting block')
            print(block)

        print('-' * 20)

    def listen_for_input(self):
        waiting_for_user_input = True

        while waiting_for_user_input:
            print('-' * 50)
            print('Please choose')
            print('1: Add a new transaction value')
            print('2: Mine new block')
            print('3: Output the blockchain blocks')
            print('4: Verify Open Transactions')
            print('q: Quit')

            user_input = self.get_user_input()

            if (user_input == '1'):
                transaction_data = self.get_transaction_data()
                recipient, amount = transaction_data
                self.blockchain.add_transaction(recipient, amount, self.id)
                BlockchainFile.save_data(self.blockchain)
            elif (user_input == '2'):
                if self.blockchain.mine_block(self.id):
                    BlockchainFile.save_data(self.blockchain)
            elif (user_input == '3'):
                self.print_blockchain_elements()
            elif (user_input == '4'):
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions!')
            elif (user_input == 'q'):
                waiting_for_user_input = False
            else:
                print('Input was invalid, please pick a value from the list!')

            if not Verification.verify_chain(self.blockchain):
                print('Invalid chain!')
                self.print_blockchain_elements()
                break

            print('-' * 50)
            current_balance = self.blockchain.get_balance(self.id)
            print(f'Balance of {self.id}: {current_balance:10.2f}')

        print('Done!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
