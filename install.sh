#!/usr/bin/env bash

exiting_code_message="some message"

chmod +x src/uninstall.sh
src/uninstall.sh
chmod +x src/dependencies.sh
src/dependencies.sh

exitcode=$?;
if [[ ${exitcode} != 0 ]]; then
    echo "couldn't install dependencies!!"
    echo "Exiting....."
    echo ${exiting_code_message}
    exit
fi

HOME="$(echo -n $(bash -c "cd ~${USER} && pwd"))"
mkdir -p ${HOME}/.linuxAI/linuxAI
cp -R . ${HOME}/.linuxAI/linuxAI/


echo "[Desktop Entry]
Name=LinuxAI
Comment=A Linux Assistant
Keywords=ai;assistant;linuxai;
Exec=$HOME/.linuxAI/linuxAI/main.py
Icon=$HOME/linuxAI/src/static/artificial_intelligence.gif
Terminal=false
Type=Application
Categories=GNOME;GTK;
StartupNotify=true
Name[en_IN]=linuxAI
">linuxAI.desktop

sudo mv linuxAI.desktop /usr/share/applications/