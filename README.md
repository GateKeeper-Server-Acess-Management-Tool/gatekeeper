#gatekeeper

> Lightweight server access management system

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/gatekeeper/blob/master/LICENSE.md)

Gatekeeper is a personalised server access management tool (and a slack bot) which keeps a track of all the administrative rights attempts (like sudo and su) on server (via SSH) and allows/disallows log-in attempts based on public key of user and logs all activity in form of slack message. It provides easy granting/revoking access to servers to team members through pull requests on a keykeeper repository.

## Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [Contact](#contact)

## Features

- Request SSH access to a server just by creating a PR to the keykeeper repository.
- Stateless and serverless.gatekeeper runs on a single binary.
- Optional server activity logs to your favourite workspace like Slack or Discord.
- Easy Installation and Configuration
- Get notified when someone escalates privileges or performs administrative tasks using `sudo` or `su`

## Dependencies

The following softwares are required for runninggatekeeper:-

- PAM
- OpenSSH server

## Installation

1. Create a keykeeper Repository using the template repository [here](https://github.com/gatekeeper/keykeeper-template).

2. Clone thegatekeeper repository

   `git clone https://github.com/gatekeeper/gatekeeper.git`

3. Change into the repository directory and build the latest binaries using Cargo

   `cargo build --release`

4. Copy `sample.config.toml` to `config.toml` and make changes to the config this way:

   ```toml
   # Hostname of the machine runninggatekeeper. Note that this should be
   # same as the file you create in the `hosts` directory in keykeeper.
   hostname = 'virtual-machine'

   # keykeeper repository configuration
   [keykeeper]

   # URL of the keykeeper repository, it should be of the format
   # `https://api.github.com/repos/<ORGANIZATION>/<keykeeper-REPOSITORY>/contents`
   base_url = 'https://api.github.com/repos/keykeeper-template/contents'

   # This should be a personal access token made by a member of organization on his/her
   # behalf who can read the keykeeper repository. Go to this
   # https://github.com/settings/tokens/new?description=keykeeper%20Token&scopes=repo
   # to make a new token with correct scopes.
   token = 'secret_token'

   # Webhook APIs corresponding to various notifiers
   [notifiers]

   # Make an incoming hook to your Slack workspace from this
   # app(https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)
   # and paste the hook URL here. You can customize the icon and name as you like.
   slack = 'https://hooks.slack.com/services/ABCDEFGHI/ABCDEFGHI/abcdefghijklmnopqrstuvwx'
   ```

5. Once you are done configuring, run this command with root(sudo) privileges

   `cd install && sudo ./install.sh`

6. Add `/opt/gatekeeper/bin` to your PATH variable.

## Usage

```
$gatekeeper --help

gatekeeper 0.1.0
Simple server access management system on a binary

USAGE:
  Gatekeeper [SUBCOMMAND]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

SUBCOMMANDS:
    auth      Authorizes users based on from keykeeper repository. This command is passed through
              `AuthorizedKeysCommand` in sshd_config.
    config    Get or setgatekeeper configuration
    help      Prints this message or the help of the given subcommand(s)
    logs      Get the globalgatekeeper logs
    ssh       Handles the PAM SSH calls by pam_exec forgatekeeper
    su        Handles the PAM su calls by pam_exec forgatekeeper
    sudo      Handles the PAM sudo calls by pam_exec forgatekeeper
```

Though most of the commands are for internal use of PAM, you can edit configuration ofgatekeeper any time

```sh
$gatekeeper config --help
```

_NOTE:_ config can be fetched/edited only with `root` (`sudo`) access.

To view logs

```sh
$gatekeeper logs --help
```

## Development

You need to have [Rust](https://www.rust-lang.org/tools/install) installed along with the mentioned [dependencies](#dependencies)

Open your favourite terminal and perform the following tasks:-

1. Clone this repository.

```bash
$ git clone https://github.com/GateKeeper-Server-Acess-Management-Tool/gatekeeper
```

2. Make the required changes inside the source code directory ([src/](src/))

3. Run `cargo test` to test your changes.

4. Rebuild the binary using `cargo build` command.
