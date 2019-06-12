#!/usr/bin/env python

import argparse
import yaml
import logging
import sys
import os
import subprocess

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

    entry_path = name.split('.')

    for level in entry_path:
        entry_set = entry_set[level]

    keys = []

    for ek, ev in entry_set.iter_items():
    
        entry_value = ev.get()

        if not entry_value:
            entry_name = ek[0]
        else:
            entry_name = entry_value

        keys.append((ek[0], entry_name))

    return keys

def initialize():

    config = load_config()
    #encryption = load_encryption(config.encryption)
    #backend = load_backend(config.backend, encryption)

    encryption = Plain(config.encryption)
    backend = Local(config.backend, encryption)

    return config, backend

def get(name, config, backend):

    entries = get_entries(name, config.bundles)

    ret = []

    for e in entries:
        entry_value = backend.get(e[1])
        if entry_value:
            ret.append((e[0].upper(), entry_value))
            #print("export %s=%s" % (e[0].upper(), entry_value))

    return ret

def clear(name, config, backend):

    entries = get_entries(name, config.bundles)

    for e in entries:
        print("unset %s" % (e.upper()))

def run_command(args, envs=[]):

    runtime_env = os.environ.copy()

    for e in envs:
        runtime_env[e[0]] = e[1]

    ret = subprocess.run(args, env=runtime_env)

def main():

    parser = argparse.ArgumentParser(description='Manage API keys and setting environment variables')
    parser.add_argument('--bundle', '-b', metavar='BUNDLENAME', help='ENV bundle to use')
    parser.add_argument('--set', metavar='NAME VALUE', help='sets ENV variable', nargs=2)
    parser.add_argument('--clear', metavar='BUNDLENAME', help='clear ENV variables from given bundles', nargs='+')

    parser.add_argument('--exec', '-e', metavar='COMMAND', nargs='*', help='Command to run')

    args = parser.parse_args()

    if (args.exec and
       not args.bundle):
       parser.error("The 'exec' option requires the 'bundle' option to be specified")

    config, backend = initialize()


    if args.set:
        kn, kv = args.set
        e = backend.set(kn, kv)

    if args.exec:

        bundles = get(args.bundle, config, backend)
        run_command(args.exec, bundles)

    if args.clear:


        if args.clear[0] == 'all':
            bundle_list = set()
            for p in config.bundles:
                bundle_list.add(p)
        else:
            bundle_list = args.clear

        for bundle in bundle_list:
            e = clear(bundle, config, backend)


# Main caller
if __name__ == '__main__':
    main()
