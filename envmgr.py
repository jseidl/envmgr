#!/usr/bin/env python

import argparse
import logging
import sys
import os
import subprocess

#from envmgr.helpers.loaders import load_backend, load_encryption
from envmgr.config import load_config
from envmgr.backends.local import Local
from envmgr.encryptions.plain import Plain
from envmgr.encryptions.aes import AES
from envmgr.constants import ENVMGR_HOME, ENVMGR_CONFIG, ENVMGR_HOME_PERM

LOGGER = logging.getLogger(__name__)

def abort(error_code=-1):
    sys.exit(error_code)

def get_entries(name, entry_set):

    entry_path = name.split('.')

    for level in entry_path:
        entry_set = entry_set[level]

    keys = []

    for ek, ev in entry_set.items():
    
        if isinstance(ev, dict):
            raise AttributeError("Selected bundle is not a leaf node")

        entry_value = ev

        if not entry_value:
            entry_name = ek
        else:
            entry_name = entry_value

        keys.append((ek, entry_name))

    return keys

def initialize():

    config = load_config()
    #encryption = load_encryption(config.encryption)
    #backend = load_backend(config.backend, encryption)

    encryption = AES(config)
    #encryption = Plain(config.encryption)
    backend = Local(config, encryption)

    return config, backend

def get(name, config, backend):

    entries = get_entries(name, config['bundles'])

    ret = []

    for e in entries:
        entry_value = backend.get(e[1])
        if entry_value:
            ret.append((e[0].upper(), entry_value))

    return ret

def export(bundle):

    for env in bundle:
        print("export %s=\"%s\"" % (env[0],env[1]))

def clear(bundle):

    for e in bundle:
        print("unset %s" % (e[0].upper()))

def run_command(args, envs=[]):

    runtime_env = os.environ.copy()

    for e in envs:
        runtime_env[e[0]] = e[1]

    ret = subprocess.run(args, env=runtime_env, cwd=os.getcwd())

def main():

    parser = argparse.ArgumentParser(description='Manage API keys and setting environment variables')

    # ENV vault related options
    # @FIXME nargs looks wrong.. maybe regular with parameter being NAME=VALUE, then split?
    parser.add_argument('--set', '-s', metavar='NAME VALUE', help='Sets ENV variable', nargs=2)

    # Bundle related options
    parser.add_argument('--bundle', '-b', metavar='BUNDLENAME', help='ENV bundle to use')
    parser.add_argument('--clear', '-c', action='store_true', help='Clear ENV variables from given bundle')

    parser.add_argument('--export', '-x', action='store_true', help='Return BASH-compatible export statements')
    parser.add_argument('--exec', '-e', metavar='COMMAND', nargs='*', help='Execute a command with the environment variables set.')

    args = parser.parse_args()

    # Check if bundle option is set both --exec and --export
    if (any((args.exec, args.export, args.clear)) and
       not args.bundle):
       parser.error("'bundle' option is required for this action.")

    config, backend = initialize()

    if args.set:
        kn, kv = args.set
        return backend.set(kn, kv)

    # Load bundle for bundle-related options
    try:
        bundle = get(args.bundle, config, backend)
    except AttributeError as e:
        LOGGER.error("Error selecting bundle: %s", str(e))
        abort()

    if args.exec:
        return run_command(args.exec, bundle)

    if args.export:
        return export(bundle)

    if args.clear:
        return clear(bundle)

# Main caller
if __name__ == '__main__':
    main()
