from pathlib import Path

ENVMGR_FOLDER = '.envmgr'
ENVMGR_HOME = Path(Path.home(), ENVMGR_FOLDER)
ENVMGR_HOME_PERM = 0o700
ENVMGR_CONFIG = 'envmgr.yml'
ENVMGR_CONFIG_PATH = Path(ENVMGR_HOME, ENVMGR_CONFIG)

COMPONENT_BACKEND = 'backends'
COMPONENT_ENCRYPTION = 'encryptions'
