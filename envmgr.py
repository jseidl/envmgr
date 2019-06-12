import argparse
import yaml
import logging
import sys

from configmanager import Config
from pathlib import Path

#from envmgr.helpers.loaders import load_backend, load_encryption
from envmgr.backends.local import Local
from envmgr.encryptions.plain import Plain
from envmgr.constants import ENVMGR_HOME, ENVMGR_CONFIG, ENVMGR_HOME_PERM

LOGGER = logging.getLogger(__name__)

def abort(error_code=-1):
    sys.exit(error_code)

def create_default_config():

    LOGGER.info('Creating default configuraiton file')

def load_config():

    home_path = ENVMGR_HOME

    if not home_path.exists():
        LOGGER.info('envmgr folder is missing. Trying to create')
        home_path.mkdir(mode=ENVMGR_HOME_PERM)
        LOGGER.info('envmgr folder created at %s', ENVMGR_HOME)

    config_path = Path(home_path, ENVMGR_CONFIG)

    if not config_path.exists():
        LOGGER.info('Configuration file missing, creating default config file')
        create_default_config()

    try:
        # Load config
        with open(config_path, 'r') as c:
            config_object = yaml.load(c, yaml.SafeLoader)
            config = Config(config_object)

        return config

    except yaml.YAMLError as e:
        LOGGER.error("Error loading configuration file: %s", str(e))
        abort()

def get_entries(name, entry_set):

    entry_set = entry_set[name]

    keys = []

    for ek, ev in entry_set.iter_items():
    
        entry_value = ev.get()

        if not entry_value:
            entry_name = ek[0]
        else:
            entry_name = value

        keys.append(entry_name)

    return keys

def initialize():

    config = load_config()
    #encryption = load_encryption(config.encryption)
    #backend = load_backend(config.backend, encryption)

    encryption = Plain(config.encryption)
    backend = Local(config.backend, encryption)

    return config, backend

def get(name, config, backend):

    entries = get_entries(name, config.providers)

    for e in entries:
        entry_value = backend.get(e)
        if entry_value:
            print("export %s=%s" % (e.upper(), entry_value))

def clear(name, config, backend):

    entries = get_entries(name, config.providers)

    for e in entries:
        print("unset %s" % (e.upper()))

def main():

    parser = argparse.ArgumentParser(description='Manage API keys and setting environment variables')
    parser.add_argument('--get', metavar='BUNDLENAME', help='ENV bundle to get')
    parser.add_argument('--set', metavar='NAME VALUE', help='sets ENV variable', nargs=2)
    parser.add_argument('--clear', metavar='BUNDLENAME', help='clear ENV variables from given bundles', nargs='+')

    args = parser.parse_args()

    config, backend = initialize()

    if args.get:
        e = get(args.get, config, backend)

    if args.set:
        kn, kv = args.set
        e = backend.set(kn, kv)

    if args.clear:


        if args.clear[0] == 'all':
            provider_list = set()
            for p in config.providers:
                provider_list.add(p)
        else:
            provider_list = args.clear

        for provider in provider_list:
            e = clear(provider, config, backend)


# Main caller
if __name__ == '__main__':
    main()
