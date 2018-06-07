#!/usr/bin/env bash

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

sed -i "1s/.*/#\!\/usr\/bin\/env \/home\/$USER\/env\/bin\/python/" main.py
export GOOGLE_APPLICATION_CREDENTIALS="/home/$USER/Robot/src/credentials/service_account/apis-5ecec14be349.json"
gcloud auth login