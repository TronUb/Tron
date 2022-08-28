#!/bin/bash



oname=$(uname -o)

if [ "$oname" == "Android" ]; then
    clear
    echo "Starting Tron Deployment (Termux) . . ."
else
    python3 -m main
