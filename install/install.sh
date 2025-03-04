#!/bin/bash

# Install all the files at right place
mkdir -p /opt/gatekeeper/bin
mkdir -p /opt/gatekeeper/logs
touch /opt/gatekeeper/logs/sudo.logs
touch /opt/gatekeeper/logs/su.logs
touch /opt/gatekeeper/logs/ssh.logs
mkdir -p /opt/gatekeeper/custom-logs
touch /opt/gatekeeper/custom-logs/ssh.logs
touch /opt/gatekeeper/custom-logs/sudo.logs
touch /opt/gatekeeper/custom-logs/su.logs
touch /opt/gatekeeper/custom-logs/auth.logs

cp ../target/release/gatekeeper /opt/gatekeeper/bin/gatekeeper
chown root /opt/gatekeeper/bin/gatekeeper
chgrp root /opt/gatekeeper/bin/gatekeeper
chmod  700 /opt/gatekeeper/bin/gatekeeper

cp ../config.toml /opt/gatekeeper/config.toml
chmod 700 /opt/gatekeeper/config.toml

# edit `sshd_config` file
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.gatekeeper.bak
python3 edit-sshd-config.py
cp gatekeeper_tmp_sshd_config /etc/ssh/sshd_config
rm gatekeeper_tmp_sshd_config
service sshd restart

# installing pam_exec lines
python3 pam-install-sudo.py
python3 pam-install-su.py
python3 pam-install-ssh.py

cp gatekeeper_tmp_sudo /etc/pam.d/sudo
cp gatekeeper_tmp_su /etc/pam.d/su
cp gatekeeper_tmp_ssh /etc/pam.d/sshd

rm gatekeeper_tmp_sudo
rm gatekeeper_tmp_su
rm gatekeeper_tmp_ssh
