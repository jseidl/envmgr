import logging

from abc import ABC

class Component(ABC):
    
    config = None
    logger = None

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.setup()

    def setup():
        pass

class Backend(Component):

    encryption = None

    def __init__(self, config, encryption):
        self.encryption = encryption
        super().__init__(config)

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

class Encryption(ABC):

    def __init__(self, config):
        super()

    def encrypt(self, data):
        raise NotImplementedError

    def decrypt(self, data):
        raise NotImplementedError
