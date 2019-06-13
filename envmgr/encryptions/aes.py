import hashlib
import binascii

from os import urandom
from miscreant.aes.siv import SIV

from envmgr.models import Encryption

SALT_SIZE = 8 # bytes
NONCE_SIZE = 16
PBKDF2_HASH = 'sha256'
PBKDF2_ITERATIONS = 100000

class AES(Encryption):

    default_options = {
        'salt': None,
        'nonce': None
    }

    pubkey = None

    def setup(self):

        password = self.ask_password()

        # Generate Salt & Nonce
        if not self.config['salt']:
            salt = urandom(SALT_SIZE)
            self.config['salt'] = binascii.hexlify(salt)
        if not self.config['nonce']:
            nonce = urandom(NONCE_SIZE)
            self.config['nonce'] = binascii.hexlify(nonce)

        # Derive key from password and initialize SIV
        key = self.derive_key(password)
        self.engine = SIV(key)

    def derive_key(self, password):

        salt = binascii.unhexlify(self.config['salt'])
        pw_bytes = bytes(password, 'utf-8')
        dk = hashlib.pbkdf2_hmac(PBKDF2_HASH, pw_bytes, salt, PBKDF2_ITERATIONS)
        return dk

    def encrypt(self, data):

        nonce = binascii.unhexlify(self.config['nonce'])
        return self.engine.seal(data, [nonce])
    
    def decrypt(self, data):

        nonce = binascii.unhexlify(self.config['nonce'])
        return self.engine.open(data, [nonce])
