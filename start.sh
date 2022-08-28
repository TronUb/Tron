#!/bin/bash



oname=$(uname -n)
filename="./config.txt"
repo="https://github.com/TronUb/Tron.git"
ffmpeg=$(ffmpeg)
nodejs=$(node)
python=$(python3 --version)
pip=$(pip --version)
pytgcalls=$(pip3 show py-tgcalls)
git=$(git)


# not found
no_file="No such file or directory"
no_cmd="not found"


echo $'Welcome to Tron Corporation\n'

if [ "$oname" == "localhost" ]; then
    clear
    # update & upgrade ubuntu
    apt update && apt upgrade

    # install python3
    if [[ $python =~ no_cmd ]]; then
       echo $'Installing python3 . . .\n'
       apt install python3
       clear
    fi

    # install python3 pip
    if [[ $pip =~ no_cmd ]]; then
       echo $'Installing python3 pip . . .\n'
       apt install pip
       clear
    fi

    # install git 
    if [[ $git =~ no_file ]]; then
        echo $'Installing git . . .\n'
        apt install git
        clear
    fi

    # clone Tron repo
    if [ ! -f "$filename" ]; then
        git clone $repo
        clear
        cd Tron
    else
        cd Tron
    fi

    # install ffmpeg
    if [[ $ffmpeg =~ $error ]]; then
        apt install ffmpeg
        clear
    fi

    # install nodejs
    if [[ $nodejs =~ $error ]]; then
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
