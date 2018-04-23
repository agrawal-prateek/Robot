#!/usr/bin/env bash

exiting_code_message="some message"

chmod +x src/uninstall.sh
src/uninstall.sh
chmod +x src/dependencies.sh
src/dependencies.sh

HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
mkdir -p ${HOME}/.linuxAI/linuxAI
cp -R . ${HOME}/.linuxAI/linuxAI/

exitcode=$?;
if [[ ${exitcode} != 0 ]]; then
    echo "couldn't install dependencies!!"
    echo "Exiting....."
    echo ${exiting_code_message}
    exit
fi
