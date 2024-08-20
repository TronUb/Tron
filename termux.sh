#!/bin/bash


# File containing the list of required packages
REQUIREMENTS_FILE="requirements.txt"

# Windows fails to install Tgcrypto, it shouldnt be
# added to the same requirements.txt file
install_tgcrypto() {
    TGCRYPTO="TgCrypto"

    if pip show "$TGCRYPTO" &> /dev/null; then
        echo "$TGCRYPTO is installed."
    else
        echo "$TGCRYPTO is not installed, Trying to install ..."
    fi
}

# Function to check and install Python 3
install_python() {
    if command -v python3 &> /dev/null; then
        echo "Python3 is installed."
    else
        echo "Python3 is not installed. Trying to install Python3 ..."

        # Install Python 3
        echo "Installing Python3  ..."
        if apt install -y python3; then
            echo "Python3 successfully installed."
        else
            echo "Failed to install Python3. Please check your package manager or permissions."
            exit 1
        fi
    fi
}

install_numpy() {
    MATHLIB="m" pkg install python-numpy
}

install_xml() {
    apt install libxml2 libxslt
    CFLAGS='-O0' python3 -m pip install lxml
}

install_psycopg2() {
    apt install postgresql python make clang
    python3 -m pip install psycopg2
}

install_pillow() {
    apt install libjpeg-turbo
    LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/"
    python3 -m pip install pillow
}

install_ffmpeg() {
    apt install ffmpeg
}

install_userbot_dependencies() {
    # Check if the requirements file exists
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "Requirements file not found!"
        exit 1
    fi

    # Read each line from the requirements file
    while IFS= read -r package
    do
        # Skip empty lines and comments
        [[ "$package" =~ ^\s*$ || "$package" =~ ^\s*# ]] && continue

        # Check if the package is installed
        if pip show "$package" &> /dev/null; then
            echo "$package is installed."
        else
            echo "$package is not installed, Trying to install ..."
        fi
    done < "$REQUIREMENTS_FILE"
}

update_terminal() {
    echo "Updating package lists ..."
    apt update

    echo "Upgrading installed packages ..."
    apt upgrade -y

    echo "Updating system ..."
    apt dist-upgrade -y

    echo "Cleaning up ..."
    apt autoremove -y

    echo "Update complete."

    clear
}

run_userbot() {
    python3 -m main
}

main() {
    update_terminal
    install_python
    install_userbot_dependencies
    run_userbot
}

main
