# envmgr - Environment Variables Manager
Safely and easily manage service API keys to be used as environment variables

## Security model

### What are we trying to achieve?
Store API secrets securely either on a local file or remote backend.

### What powers an adversary have to subvert those resources?
An attacker might have access to the disk or S3 bucket where the vault is laying on, or able to intercept at transit.

### What security properties we wish to achieve?
We wanna make sure the attacker cannot retrieve your vault's secrets neither at rest nor at transit (when using remote backends)

### Considerations & Current Known Security Issues
There's no relibable way to erase data from memory on python as strings are immutable. Envmgr does **NOT** protect your secrets from memory snooping. Maybe someday I'll rewrite this in a language that allows that. :)

## Usage

    usage: envmgr [-h] [--set ENTRYKEY=ENTRYVALUE [ENTRYKEY=ENTRYVALUE ...]]
                  [--list] [--reveal] [--delete ENTRYKEY] [--bundle BUNDLENAME] [--clear]
                  [--export] [--exec ...]

    Manage API keys and setting environment variables

    optional arguments:
      -h, --help            show this help message and exit
      --set ENTRYKEY=ENTRYVALUE [ENTRYKEY=ENTRYVALUE ...], -s ENTRYKEY=ENTRYVALUE [ENTRYKEY=ENTRYVALUE ...]
                            Sets ENV variable
      --list, -l            Lists current vault items, with values redacted.
      --reveal, -r          Reveals secret values on --list action.
      --delete ENTRYKEY, -d ENTRYKEY
                            Vault entry key to delete
      --bundle BUNDLENAME, -b BUNDLENAME
                            ENV bundle to use
      --clear, -c           Clear ENV variables from given bundle
      --export, -x          Return BASH-compatible export statements
      --exec ..., -e ...    Execute a command with the environment variables set.


### Before you start

There's no installation script yet, is useful to link `envmgr.py` to `/usr/bin`

    $ sudo ln -s <PATH_TO_ENVMGR>/envmgr.py /usr/bin/envmgr

### Configuration

All `envmgr` data will be stored on `$HOME/.envmgr`. Upon running `envmgr` for the first time, it will create the home directory and configuration file with default options, if none is present.

#### Backends

The backend is where your secrets are stored (also refered to as 'vaults'). Currently only the `local` backend provider is implemented, which is a `msgpack`-serialized python dictionary. Make sure you have selected an encryption scheme other than `plain` or your secrets will be exposed at rest, defeating what `envmgr` tries to achieve.

Available backends:
* Local

Under construction:
* AWS S3 Buckets
* KeePassX keychains
* 1password keychains

#### Encryptions

The default encryption scheme is `AES SIV` (thanks @evq). If this is your first time running, it will ask you for a password (once) and use that to generate your `nonce` (for AES-SIV encryption and decryption) and `salt` for `ARGON2Id` (thanks @Riastradh) used for key-derivation. **If you lose your password you WONT be able to recover your vault**

Each entry value on your vault is encrypted by itself, then the whole vault is encrypted again, to protect your entry names.

There's a `plain` encryption scheme which disables encryption. This is useful if your backend provider (password managers, S3 buckets) already provide encryption and you don't want to double encrypt. **Be careful when using this.**

Available encryption:
* AES-SIV + ARGON2Id (aes)

Under construction:
* GPG (gpg)

### Using `envmgr`

#### Adding secrets to your vault

Use the `--set` flag to add values to the vault

    $ envmgr --set secret_name=secret_value secret2_name=secret2_value # (...)

#### Removing secrets from the vault

Use the `--delete` flag to remove values from the vault

    $ envmgr --delete secret_name

#### Listing your secrets

Use the `--list` flag to list all secret values partially redacted on the vault

    $ envmgr --list

If you wish to see the full values, pass `--reveal` to the above command.

    $ envmgr --list --reveal

#### Using your secrets

`envmgr` uses the concept of 'bundles', which groups secrets and assigns
each of them to a given environment variable.

You can have multiple levels of hierarchy, which for now doesn't adds much other than organization. You can have for example:

    * mycompany
      * production
          cloudflare_token: production/cloudflare/token
      * staging
          cloudflare_token: staging/cloudflare/token

And call them by specifying the `--bundle` parameter:

    $ envmgr --bundle mycompany.production --exec env

`envmgr` supports both calling the command you want to run and passing the environment variables directly to this subprocess environment OR printing `export` statements so you can source into your shell

    $ source <(envmgr --bundle mycompany.production --export)


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
        salt: !!binary |
          YThkYjNmZjdhNmY1ZjU1Mg==

## To-do's
* Encryption / GPG asymmetric
* Backend / AWS S3
* Backend / 1password
* Backend / KeepassX
