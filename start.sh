#!/bin/bash

uname=$(uname -n)
filename="./config.txt"
repo="https://github.com/TronUb/Tron.git"
pytgcalls=$(pip3 show py-tgcalls)


# not found
no_cmd="not found"


installed() {
    return $(dpkg-query -W -f '${Status}\n' "${1}" 2>&1|awk '/ok installed/{print 0;exit}{print 1}')
}


clear
echo $'Welcome to Tron Corporation\n'
sleep 3


if [ "$uname" == "localhost" ]; then
    clear
    # update & upgrade ubuntu
    echo $'Updating & Upgrading ubuntu apt . . .\n'
    apt update && apt upgrade
    clear

    # install python3
    if ! installed python3; then
       echo $'Installing python3 . . .\n'
       apt install python3
       clear
    fi

    # install python3 pip
    if ! installed pip; then
       echo $'Installing python3 pip . . .\n'
       apt install pip
       clear
    fi

    # install git 
    if ! installed git; then
        echo $'Installing git . . .\n'
        apt install git
        clear
    fi

    # install ffmpeg
    if ! installed ffmpeg; then
        apt install ffmpeg
        clear
    fi

    # install nodejs
    if ! installed nodejs; then
        bash installl_nodejs.sh
        clear
    fi

    # install py-tgcalls
    if [[ $pytgcalls =~ no_cmd ]]; then
        echo 'Installing py-tgcalls . . .\n'
        python3 -m pip install py-tgcalls
        clear
    fi

    python3 -m main
else
    python3 -m main
fi
