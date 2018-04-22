#!/usr/bin/env bash

#HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
#MODEL="$(jq '.model' $HOME/.linuxAI/details.json)"

MODEL="linuxai-200815-linux-ai-znrszd"
googlesamples-assistant-pushtotalk --project-id linux-ai --device-model-id ${MODEL}