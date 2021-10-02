from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
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
                self.private_key = keys[1]
        except (IOError, IndexError):
            print('Loading wallet failed...')

    def generate_keys(self):
        generated_key = RSA.generate(1024)
        binary_public_key = generated_key.publickey().exportKey(format='DER')
        binary_private_key = generated_key.exportKey(format='DER')
        ascii_private_key = binascii.hexlify(binary_private_key).decode('ascii')
        ascii_public_key = binascii.hexlify(binary_public_key).decode('ascii')

        return (ascii_private_key, ascii_public_key)

    def sign_transaction(self, sender, recipient, amount):
        encoded_transaction = (str(sender) + str(recipient) + str(amount)).encode('utf8')
        encrypted_trasaction = SHA256.new(encoded_transaction)

        binary_private_key = binascii.unhexlify(self.private_key)
        rsa_private_key = RSA.import_key(binary_private_key)

        signer = PKCS1_v1_5.new(rsa_private_key)
        signature = signer.sign(encrypted_trasaction)
        ascii_signature = binascii.hexlify(signature).decode('ascii')

        return ascii_signature

    
    @staticmethod
    def verify_transaction(transaction):
        encoded_transaction = (str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8')
        encrypted_transaction = SHA256.new(encoded_transaction)

        binary_public_key = binascii.unhexlify(transaction.sender)
        rsa_public_key = RSA.import_key(binary_public_key)

        verifier = PKCS1_v1_5.new(rsa_public_key)
        binary_signature = binascii.unhexlify(transaction.signature)

        return verifier.verify(encrypted_transaction, binary_signature)


    