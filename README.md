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
    providers:
        cloudflare:
            default:
                cloudflare_email: cloudflare/email
                cloudflare_token: cloudflare/token
                cloudflare_org_id: cloudflare/orgid
        fastly:
            default:
                fastly_api_token:

    encryption:
        plain:
    
    backend:
        local:

## To-do's
* Encryption / AES symmetric
* Encryption / GPG asymmetric
* Backend / AWS S3
* Backend / 1password
* Backend / KeepassX
