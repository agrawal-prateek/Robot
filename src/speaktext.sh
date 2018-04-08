#!/usr/bin/env bash

# give firsh command line argument as a string to speak

export GOOGLE_APPLICATION_CREDENTIALS='src/credentials/texttospeech/linuxAI-49241010769b.json'
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
}" "https://texttospeech.googleapis.com/v1beta1/text:synthesize" > "src/temp/synthesizeoutput.txt"

audiobase=$(jq -r .audioContent src/temp/synthesizeoutput.txt)
echo $audiobase>src/temp/synthesizeoutput.txt

base64 src/temp/synthesizeoutput.txt --decode > src/temp/synthesizedaudio.mp3
mpg123 src/temp/synthesizedaudio.mp3