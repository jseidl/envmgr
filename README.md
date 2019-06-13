# envmgr - Environment Variables Manager
Safely and easily manage service API keys to be used as environment variables

## Usage
    usage: envmgr.py [-h] [--bundle BUNDLENAME] [--set NAME VALUE NAME VALUE]
                     [--clear BUNDLENAME [BUNDLENAME ...]]
                     [--exec [COMMAND [COMMAND ...]]]

    Manage API keys and setting environment variables

    optional arguments:
      -h, --help            show this help message and exit
      --bundle BUNDLENAME, -b BUNDLENAME
                            ENV bundle to use
      --set NAME VALUE NAME VALUE
                            sets ENV variable
      --clear BUNDLENAME [BUNDLENAME ...]
                            clear ENV variables from given bundles
      --exec [COMMAND [COMMAND ...]], -e [COMMAND [COMMAND ...]]
                            Command to run

## Example config
    backend:
      options: {}
      provider: local
    bundles:
      myproject:
        production:
          cloudflare_email: cloudflare/email
          cloudflare_token: cloudflare/token
          fastly_api_key: fastly/token
    encryption:
      provider: aes
      options:
        nonce: !!binary |
          ODRjYTJlZTU0OTE4NDUwNmVjNjI2MGE1NDY5ZjYyNWY=
        salt: !!binary |
          YThkYjNmZjdhNmY1ZjU1Mg==

## To-do's
* Encryption / GPG asymmetric
* Backend / AWS S3
* Backend / 1password
* Backend / KeepassX
