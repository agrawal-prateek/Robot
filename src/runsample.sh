#!/usr/bin/env bash

#HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
#MODEL="$(jq '.model' $HOME/.linuxAI/details.json)"

MODEL="linuxai-200815-linux-ai-znrszd"
DEVICE="a052c58c-3dac-11e8-9cf3-2c6e851f5f04"
#googlesamples-assistant-pushtotalk --project-id linux-ai --device-model-id ${MODEL}
#python src/grpc/pushtotalk.py --project-id linux-ai --device-model-id ${MODEL}
python src/grpc/textinput.py --device-model-id ${MODEL} --device-id ${DEVICE}