# api-vault
Safely and easily manage service API keys to be used as environment variables

## Usage
    usage: apivault.py [-h] [--get BUNDLENAME] [--set NAME VALUE NAME VALUE]
                   [--clear BUNDLENAME [BUNDLENAME ...]]
    
    Manage API keys and setting environment variables
    
    optional arguments:
      -h, --help            show this help message and exit
      --get BUNDLENAME      ENV bundle to get
      --set NAME VALUE NAME VALUE
                        sets ENV variable
      --clear BUNDLENAME [BUNDLENAME ...]
                        clear ENV variables from given bundles
