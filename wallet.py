from Crypto.PublicKey import RSA
import binascii

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        try:
            with open('wallet.txt', mode='w') as f:
                f.write(self.public_key)
                f.write('\n')
                f.write(self.private_key)
        except (IOError, IndexError):
            print('Saving wallet failed...')

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1][:-1]
        except (IOError, IndexError):
            print('Loading wallet failed...')

    def generate_keys(self):
        generated_key = RSA.generate(1024)
        binary_public_key = generated_key.publickey().exportKey(format='DER')
        binary_private_key = generated_key.exportKey(format='DER')
        ascii_private_key = binascii.hexlify(binary_private_key).decode('ascii')
        ascii_public_key = binascii.hexlify(binary_public_key).decode('ascii')

        return (ascii_private_key, ascii_public_key)

    def save_wallet(self):
        pass

    def load_wallet(self):
        pass