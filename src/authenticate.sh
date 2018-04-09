#!/usr/bin/env bash
HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
source $HOME/.linuxAI/env/bin/activate

# Constants
CREDENTIALS=src/credentials/registerdevice/credentials.json
CLIENT_SECRET=src/credentials/registerdevice/client_secret_952663562026-5eeu4c9am3ovdod42rtb5otp20bk2mv2.apps.googleusercontent.com.json
MANUFACTURER=prateek
PRODUCT_NAME=linux-ai
DESCRIPTION=A-Artificial-Intelligence-For-Linux

# Generate credentials
google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype --client-secrets ${CREDENTIALS} --save

# Get Device Type

read -p "Enter Your Device Type (LIGHT, SWITCH or OUTLET): " DEVICE_TYPE


# Generate Random Model
MODEL="$(openssl rand -hex 16)"

cp ${CLIENT_SECRET} .
cp ${CREDENTIALS} .
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

rm credentials.json
rm client_secret_952663562026-5eeu4c9am3ovdod42rtb5otp20bk2mv2.apps.googleusercontent.com.json
gcloud auth activate-service-account --key-file="src/credentials/texttospeech/linuxAI-49241010769b.json"
