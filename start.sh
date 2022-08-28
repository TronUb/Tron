#!/bin/bash

uname=$(uname -n)
filename="./config.txt"
repo="https://github.com/TronUb/Tron.git"
pytgcalls=$(pip3 show py-tgcalls)
G='\033[0;32m'


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
    echo -e '${G}Updating & Upgrading ubuntu apt . . .${G}\n'
    apt update && apt upgrade
    clear

    # install python3
    if ! installed python3; then
       echo -e '${G}Installing python3 . . .${G}\n'
       apt install python3
       clear
    fi

    # install python3 pip
    if ! installed pip; then
       echo -e '${G}Installing python3 pip . . .${G}\n'
       apt install pip
       clear
    fi

    # install git 
    if ! installed git; then
        echo -e '${G}Installing git . . .${G}\n'
        apt install git
        clear
    fi

    # install ffmpeg
    if ! installed ffmpeg; then
        echo -e '${G}Installing ffmpeg . . .${G}\n'
        apt install ffmpeg
        clear
    fi

    # install nodejs
    if ! installed nodejs; then
        echo -e '${G}Installing nodejs . . .${G}\n'
        bash install_nodejs.sh
        clear
    fi

    # install py-tgcalls
    if [[ $pytgcalls =~ no_cmd ]]; then
        echo -e '${G}Installing py-tgcalls . . .${G}\n'
        python3 -m pip install py-tgcalls
        clear
    fi

    python3 -m main
else
    python3 -m main
fi
