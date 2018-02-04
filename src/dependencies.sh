#!/usr/bin/env bash

mkdir -p /opt/linuxAI

# Install Packages and create venv
sudo apt-get update
sudo apt-get install python3-dev python3-venv
python3 -m venv /opt/linuxAI/env
python3 -m pip install --upgrade pip
/opt/linuxAI/env/bin/python -m pip install --upgrade pip setuptools
source /opt/linuxAI/env/bin/activate

sudo apt-get install portaudio19-dev libffi-dev libssl-dev
python -m pip install --upgrade google-assistant-library
python -m pip install --upgrade google-assistant-sdk[samples]

# Install or update the authorization tool
python -m pip install --upgrade google-auth-oauthlib[tool]

# install google-cloud-sdk
if ! [ -x "$(command -v gcloud)" ]; then
  tar -xvzf src/lib/google-cloud-sdk.tar.gz -C /opt/linuxAI
  /opt/linuxAI/google-cloud-sdk/install.sh
  ln -s /opt/linuxAI/google-cloud-sdk/bin/gcloud /usr/bin/gcloud
fi

# install google-cloud-speech python library
python -m pip install --upgrade google-cloud-speech==0.30.0

# install PortAudio C/C++ library
tar -xvzf src/lib/portaudio.tar.gz -C /tmp
cd /tmp/portaudio
./configure
make
make install
cd -
rm -rf /tmp/portaudio

# install PyAudio-0.2.11 python library
tar -xvzf src/lib/PyAudio-0.2.11.tar.gz -C /tmp
cd /tmp/PyAudio-0.2.11
python setup.py install
cd -
rm -rf /tmp/PyAudio-0.2.11
