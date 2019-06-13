import logging

from configmanager import Config
from abc import ABC

from envmgr.config import save_config, DEFAULT_CONFIG

class Component(ABC):
    
    name = None
    component_type = None

    config = None
    logger = None
    default_options = {}

    def __init__(self, config):
        
        self.name = self.__class__.__name__.lower()
        self.logger = logging.getLogger(__name__)

        self.config = config[self.component_type]['options']

        if not self.config:
            self.config = self.default_options

        self.setup()

        config[self.component_type]['options'] = self.config

        # Save config after setup
        save_config(config)
    
    def setup(self):
        pass

class Backend(Component):

    component_type = 'backend'
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

class Encryption(Component):

    component_type = 'encryption'
    engine = None

    def __init__(self, config):
        super().__init__(config)

    def encrypt(self, data):
        raise NotImplementedError

    def decrypt(self, data):
        raise NotImplementedError
