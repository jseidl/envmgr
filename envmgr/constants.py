from pathlib import Path

ENVMGR_FOLDER = '.apivault'
ENVMGR_HOME = Path(Path.home(), ENVMGR_FOLDER)
ENVMGR_HOME_PERM = 0o700
ENVMGR_CONFIG = 'apivault.yml'
