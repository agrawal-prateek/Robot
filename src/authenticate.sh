#!/usr/bin/env bash
HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
source /home/prateek/$HOME/env/bin/activate

# Constants
CLIENT_SECRETS=src/.config/client_secret_71131800372-dop7miagipbqink2ecnr33so61q3li0t.apps.googleusercontent.com.json
MANUFACTURER=prateek
PRODUCT_NAME=linux-ai
DESCRIPTION=A-Artificial-Intelligence-For-Linux

# Generate credentials
google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --client-secrets ${CLIENT_SECRETS} --save

# Get Device Type
echo
read -p "Enter Your Device Type (LIGHT, SWITCH or OUTLET): " DEVICE_TYPE
echo

# Generate Random Model
MODEL="$(openssl rand -hex 16)"

cp ${CLIENT_SECRETS} .

# Register Device Modal
googlesamples-assistant-devicetool register-model --manufacturer ${MANUFACTURER} --product-name ${PRODUCT_NAME} --description ${DESCRIPTION} --type ${DEVICE_TYPE} --model ${MODEL}

# Save Data

mkdir -p $HOME/.linuxAI
rm -f $HOME/.linuxAI/details.json
touch $HOME/.linuxAI/details.json
cat <<EOF > $HOME/.linuxAI/details.json
{
    "manufacturer":"${MANUFACTURER}",
    "product-name":"${PRODUCT_NAME}",
    "description":"${DESCRIPTION}",
    "type":"${DEVICE_TYPE}",
    "model":"${MODEL}"
}
EOF

gcloud auth activate-service-account --key-file="src/credentials/texttospeech/linuxAI-49241010769b.json"
