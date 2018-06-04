#!/usr/bin/env bash

# give firsh command line argument as a string to speak

curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) -H "Content-Type: application/json; charset=utf-8" --data "{
  'input':{
    'text':'$1'
  },
  'voice':{
    'languageCode':'en-US',
    'name':'en-US-Wavenet-E',
    'ssmlGender':'FEMALE'
  },
  'audioConfig':{
    'audioEncoding':'MP3'
  }
}" "https://texttospeech.googleapis.com/v1beta1/text:synthesize" > "/home/$USER/Robot/src/temp/synthesizeoutput.txt"

audiobase=$(jq -r .audioContent /home/$USER/Robot/src/temp/synthesizeoutput.txt)
echo $audiobase>/home/$USER/Robot/src/temp/synthesizeoutput.txt

base64 /home/$USER/Robot/src/temp/synthesizeoutput.txt --decode > /home/$USER/Robot/src/temp/synthesizedaudio.mp3
mpg123 /home/$USER/Robot/src/temp/synthesizedaudio.mp3