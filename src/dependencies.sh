#!/usr/bin/env bash

HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
mkdir -p $HOME/.linuxAI

# Install Packages and create env
sudo apt-get update
sudo apt-get install python3-dev python3-venv
python3 -m pip install --upgrade pip
python3 -m venv $HOME/.linuxAI/env
$HOME/.linuxAI/env/bin/python -m pip install --upgrade pip setuptools
source $HOME/.linuxAI/env/bin/activate

sudo apt-get install portaudio19-dev libffi-dev libssl-dev
python -m pip install --upgrade google-assistant-library
python -m pip install --upgrade google-assistant-sdk[samples]

# Install or update the authorization tool
python -m pip install --upgrade google-auth-oauthlib[tool]

# install google-cloud-sdk
if ! [ -x "$(command -v gcloud)" ]; then
  tar -xvzf src/lib/google-cloud-sdk.tar.gz -C $HOME/.linuxAI
  $HOME/.linuxAI/google-cloud-sdk/install.sh
  sudo ln -s $HOME/.linuxAI/google-cloud-sdk/bin/gcloud /usr/bin/gcloud
fi

# install google-cloud-speech python library
python -m pip install --upgrade google-cloud-speech==0.30.0

# install PortAudio C/C++ library
sudo tar -xvzf src/lib/portaudio.tar.gz -C /tmp
cd /tmp/portaudio
sudo ./configure
sudo make
sudo make install
cd -
sudo rm -rf /tmp/portaudio

# install PyAudio-0.2.11 python library
sudo tar -xvzf src/lib/PyAudio-0.2.11.tar.gz -C /tmp
cd /tmp/PyAudio-0.2.11
sudo python3 setup.py install
cd -
sudo rm -rf /tmp/PyAudio-0.2.11

pip install pyaudio

if ! [ -x "$(command -v jq)" ]; then
  sudo apt-get install jq
fi