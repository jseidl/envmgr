import msgpack

from pathlib import Path

from envmgr.models import Backend
from envmgr.constants import ENVMGR_HOME

DEFAULT_VAULT_PATH = Path(ENVMGR_HOME, 'local.vault')

class Local(Backend):

    vault_path = None

    vault = None

    def setup(self):
        
        self.vault_path = DEFAULT_VAULT_PATH
        self.vault = self.load()

    def load(self):

        if not self.vault_path.exists():
            self.save()

        try:

            with open(self.vault_path, 'rb') as f:
                raw_data = self.encryption.decrypt(f.read())
                vault_object = msgpack.unpackb(raw_data, raw=False)

                return vault_object if vault_object else {}

        except Exception as e:
            self.logger.error('Failed to load vault: %s', str(e))

        return {}

    def get(self, key): 
        if key in self.vault.keys():
            return self.vault[key]

        return None

    def delete(self, key):
        self.vault.pop(key, None)
        self.save()

    def set(self, key, value):
        self.vault[key] = value
        self.save()

    def list(self):
        return self.vault

    def save(self):

        raw_data = msgpack.packb(self.vault, use_bin_type=True)
        encrypted_data = self.encryption.encrypt(raw_data)

        with open(self.vault_path, 'wb') as f:
            f.write(encrypted_data)
