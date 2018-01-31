#!/usr/bin/env bash

# install google-cloud-sdk

#if [ -x "$(command -v gcloud)" ]; then
#  rm -rf /opt/google-cloud-sdk
#  rm -f /usr/bin/gcloud
#  tar -xvzf src/lib/google-cloud-sdk.tar.gz -C /opt
#  /opt/google-cloud-sdk/install.sh
#  ln -s /opt/google-cloud-sdk/bin/gcloud /usr/bin/gcloud
#fi

# install google-cloud-speech python library
#pip install --upgrade google-cloud-speech==0.30.0

# install portaudio C/C++ library

#tar -xvzf src/lib/portaudio.tar.gz -C /tmp
#cd /tmp/portaudio
#./configure
#make
#make install
#cd -
#rm -rf /tmp/portaudio

# install PyAudio-0.2.11 python library

#tar -xvzf src/lib/PyAudio-0.2.11.tar.gz -C /tmp
#cd /tmp/PyAudio-0.2.11
#python setup.py install
#cd -
#rm -rf /tmp/PyAudio-0.2.11
