from pathlib import Path

APIVAULT_FOLDER = '.apivault'
APIVAULT_HOME = Path(Path.home(), APIVAULT_FOLDER)
APIVAULT_HOME_PERM = 0o700
APIVAULT_CONFIG = 'apivault.yml'
