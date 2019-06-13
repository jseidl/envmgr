import yaml
import logging

from configmanager import Config
from envmgr.constants import ENVMGR_CONFIG_PATH

LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'bundles': {},
    'encryption': {
        'provider': 'plain',
        'options': {}
    },
    'backend': {
        'provider': 'local',
        'options': {}
    }
}

def save_config(config):

    yaml_content = yaml.dump(config)

    with ENVMGR_CONFIG_PATH.open('w') as fh:
        fh.write(yaml_content)

def create_default_config():

    LOGGER.info('Creating default configuraiton file')
    
    save_config(DEFAULT_CONFIG)

    return DEFAULT_CONFIG

def get_home():

    home_path = ENVMGR_HOME

    if not home_path.exists():
        LOGGER.info('envmgr folder is missing. Trying to create')
        home_path.mkdir(mode=ENVMGR_HOME_PERM)
        LOGGER.info('envmgr folder created at %s', ENVMGR_HOME)

    return home_path

def load_config():


    if not ENVMGR_CONFIG_PATH.exists():
        LOGGER.info('Configuration file missing, creating default config file')
        return create_default_config()

    try:

        with ENVMGR_CONFIG_PATH.open('r') as stream:
            return yaml.safe_load(stream)

    except yaml.YAMLError as e:
        LOGGER.error("Error loading configuration file: %s", str(e))
        abort()
