#!/usr/bin/env bash

bold=$(tput bold)
normal=$(tput sgr0)

if [[ $EUID > 0 ]]; then # we can compare directly with this syntax.
  echo "Please run as root..."
  echo "type:"
  echo "${bold}sudo ./install.sh ${normal}"
  exit 1
fi
exiting_code_message="some message"

chmod +x src/uninstall.sh
src/uninstall.sh
chmod +x src/dependencies.sh
src/dependencies.sh

exitcode=$?;
if [[ ${exitcode} != 0 ]]; then
    echo "couldn't install dependencies!!"
    echo "Exiting....."
    echo ${exiting_code_message}
    exit
fi

