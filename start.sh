#!/bin/bash



oname=$(uname -o)
filename="./config.txt"

if [[ "$oname" == "Android" && ! -f "$filename" ]]; then
    clear
    echo $'Welcome To Tron Corporation.\n\n'
    echo $'Starting Tron Deployment (Termux) . . .\n\n'
    echo $'Installing Ubuntu 20 in Termux . . .\n'
    bash install_ubuntu20.sh
    clear
    echo $'Starting Ubuntu 20 . . .\n'
    bash start-ubuntu20.sh
    clear
    echo $'Updating & Upgrading Ubuntu . . .\n'
    apt update && apt upgrade 
    clear
    echo $'Installing git . . .\n'
    apt install git
    clear
    echo $'Cloning Tron Repo . . .\n'
    git clone https://github.com/TronUb/Tron.git
    clear
    echo $'Changing directory . . .\n'
    cd && cd Tron
    clear
    echo $'Installing python3 & pip3 . . .\n'
    apt install python3 python3-pip
    clear
    echo $'Installing dependencies from requirements.txt\n'
    pip3 install -r requirements.txt
    clear
    echo $'Installing nodejs . . .\n'
    bash install_nodejs.sh
    clear
    echo $'Installing ffmpeg . . .\n'
    apt install ffmpeg
    clear
    echo $'Installing py-tgcalls . . .\n'
    python -m pip install pytgcalls
    clear
    python3 -m main
elif [[ "$oname" == "Android" && -f "$filename" ]]; then
    python3 -m main
elif [ "$oname" == "Android" ]; then
    clear
    echo $'The config.txt file doesnt exist !\n'
    echo $'Set your config.txt file with config values.'
    exit
else
    python3 -m main
fi
