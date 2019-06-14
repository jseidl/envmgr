from pathlib import Path

from envmgr.models import Backend
from envmgr.constants import ENVMGR_HOME

DEFAULT_VAULT_PATH = Path(ENVMGR_HOME, "local.vault")


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

            with open(self.vault_path, "rb") as f:

                encrypted_vault = self.unserialize(f.read())
                serialized_vault = self.encryption.decrypt(encrypted_vault)
                vault_object = self.unserialize(serialized_vault)

                return vault_object if vault_object else {}

        except Exception as e:
            raise e
            self.logger.error("Failed to load vault: %s", str(e))

        return {}

    def get(self, key):

        if key in self.vault.keys():
            return self.encryption.decrypt(self.vault[key]).decode("utf-8")

        return None

    def delete(self, key):
        self.vault.pop(key, None)
        self.save()

    def set(self, key, value):
        self.vault[key] = self.encryption.encrypt(value)
        self.save()

    def list(self):
        for item_name, item_value in self.vault.items():
            yield item_name, self.get(item_name)

    def save(self):

        raw_data = self.serialize(self.vault)
        encrypted_data = self.encryption.encrypt(raw_data)
        encrypted_vault = self.serialize(encrypted_data)

        with open(self.vault_path, "wb") as f:
            f.write(encrypted_vault)
