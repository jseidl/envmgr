import binascii

from os import urandom
from miscreant.aes.siv import SIV
from argon2.low_level import hash_secret_raw, Type

from envmgr.models import Encryption

SALT_SIZE = 8  # bytes
NONCE_SIZE = 16

ARGON2_HASH_LEN = 64  # bytes
ARGON2_TIME_COST = 1  # seconds
ARGON2_MEMORY_COST = 8  # Kib
ARGON2_PARALLELISM = 1
ARGON2_TYPE = Type.ID


class AES(Encryption):

    default_options = {"salt": None}

    pubkey = None

    def setup(self):

        password = self.ask_password()

        # Generate Salt & Nonce
        if not self.config["salt"]:
            salt = urandom(SALT_SIZE)
            self.config["salt"] = binascii.hexlify(salt)

        # Derive key from password and initialize SIV
        key = self.derive_key(password)
        self.engine = SIV(key)

    def derive_key(self, password):

        salt = binascii.unhexlify(self.config["salt"])
        pw_bytes = bytes(password, "utf-8")

        dk = hash_secret_raw(
            pw_bytes,
            salt,
            time_cost=ARGON2_TIME_COST,
            memory_cost=ARGON2_MEMORY_COST,
            parallelism=ARGON2_PARALLELISM,
            hash_len=ARGON2_HASH_LEN,
            type=ARGON2_TYPE,
        )

        return dk

    def encrypt(self, data):

        nonce = urandom(NONCE_SIZE)

        if not isinstance(data, bytes):
            data = bytes(data, "utf-8")

        sealed_data = self.engine.seal(data, [nonce])

        return (sealed_data, nonce)

    def decrypt(self, payload):

        data = self.engine.open(payload[0], [payload[1]])

        return data
