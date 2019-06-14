import logging
import msgpack

from getpass import getpass
from abc import ABC

from envmgr.config import save_config


class Component(ABC):

    name = None
    component_type = None

    config = None
    logger = None
    default_options = {}

    def __init__(self, config):

        self.name = self.__class__.__name__.lower()
        self.logger = logging.getLogger(__name__)

        self.config = config[self.component_type]["options"]

        if not self.config:
            self.config = self.default_options

        self.setup()

        if self.config != config[self.component_type]["options"]:
            config[self.component_type]["options"] = self.config

            # Save config after setup
            save_config(config)

    def setup(self):
        pass


class Backend(Component):

    component_type = "backend"
    encryption = None

    def __init__(self, config, encryption):
        self.encryption = encryption
        super().__init__(config)

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

    def serialize(self, data):
        return msgpack.packb(data, use_bin_type=True)

    def unserialize(self, data):
        return msgpack.unpackb(data, raw=False)


class Encryption(Component):

    component_type = "encryption"
    engine = None

    def __init__(self, config):
        super().__init__(config)

    def ask_password(self, prompt="Password: "):

        return getpass(prompt="[envmgr] %s" % prompt)

    def encrypt(self, data):
        raise NotImplementedError

    def decrypt(self, data):
        raise NotImplementedError
