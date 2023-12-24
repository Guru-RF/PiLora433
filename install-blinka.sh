#!/bin/bash

run() {
  exec=$1
  printf "\x1b[38;5;104m --> ${exec}\x1b[39m\n"
  eval ${exec}
}

say () {
  say=$1
  printf "\x1b[38;5;220m${say}\x1b[38;5;255m\n"
}

say "Upgrading PI"
run "apt -y update"
run "apt -y upgrade"

say "Installing Prerequisites"
run "apt -y install python3-pip git"

say "Upgrading Prerequisites"
run "apt install --upgrade python3-setuptools"

say "Removing Python3 Externally Managed"
run "rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED"

say "Install Adafruit Python Shell"
run "pip3 install --upgrade adafruit-python-shell"

say "Download Blinka"
run "wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py"

say "Install Blinka"
run "python3 raspi-blinka.py