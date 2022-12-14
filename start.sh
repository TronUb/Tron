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
echo -e "${G}Welcome to Tron Corporation.\n"
sleep 3


if [ "$uname" == "localhost" ]; then
    clear
    # update & upgrade ubuntu
    echo -e "${G}Updating & Upgrading ubuntu apt . . .\n"
    apt update && apt upgrade
    clear

    # install python3
    if ! installed python3; then
       echo -e "${G}Installing python3 . . .\n"
       apt install python3
       clear
    fi

    # install python3 pip
    if ! installed pip; then
       echo -e "${G}Installing python3 pip . . .\n"
       apt install pip3
       clear
    fi

    python3 -u -m main
else
    python3 -u -m main
fi
