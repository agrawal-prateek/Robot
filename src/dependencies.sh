#!/usr/bin/env bash

HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"

# Install Packages
sudo apt-get update
sudo apt-get install -y python3-dev python3-venv
sudo apt-get install -y portaudio19-dev libffi-dev libssl-dev
sudo apt install python-gi python-gi-cairo python3-gi python3-gi-cairo gir1.2-gtk-3.0
python3 -m pip install --upgrade pip
sudo apt-get install python3-tk python-tk

tar -xvzf src/lib/google-cloud-sdk.tar.gz -C $HOME
$HOME/google-cloud-sdk/install.sh
sudo ln -s $HOME/google-cloud-sdk/bin/gcloud /usr/bin/gcloud

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

if ! [ -x "$(command -v jq)" ]; then
  sudo apt-get install -y jq
fi
if ! [ -x "$(command -v curl)" ]; then
  sudo apt install -y curl
fi
if ! [ -x "$(command -v mpg123)" ]; then
 sudo apt install -y mpg321
fi

python3 -m venv $HOME/env
$HOME/env/bin/python -m pip install --upgrade pip setuptools
source $HOME/env/bin/activate
pip install --upgrade google-assistant-library
pip install --upgrade google-assistant-sdk[samples]
pip install --upgrade google-auth-oauthlib[tool]
pip install --upgrade google-cloud-speech==0.30.0
pip install --upgrade pyaudio
pip install --upgrade google-api-python-client
pip install --upgrade oauth2client
pip install --upgrade SpeechRecognition
pip install --upgrade twilio==6.14.3
pip install --upgrade google-cloud-vision

