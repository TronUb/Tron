""" everything starts here """

import os
import socket
import platform
import subprocess
from importlib import metadata
from main.others import Colors
from config import Configuration


# check which packages are installed
installed_python_libs_file = "../installed_requirements.txt"

class Config:
    """This class generates the configs """
    pass


def isLocalHost():
    """Check if it is localhost"""
    return os.path.exists("../config.txt")


class Tools:
    """Use it for installing the required packages """
    device = platform.uname()[0].lower()
    is_linux = device=="linux"
    is_windows = device=="windows"

    @property
    def clear_screen(self):
        os.system("clear" if self.is_linux else "cls")

    def setup_config(self):
        count = 1
        self.clear_screen

        # check if the user config file exists
        if os.path.exists("config.txt"):
            print("config.txt file exists: Yes\n\n")
            with open("config.txt", "r", encoding="UTF-8") as f:
                content = [x for x in f.read().split("\n") if x not in ("\n", "")]

            # set text file config values
            print(Colors.block + "Setting configuration values.\n\n" + Colors.reset)
            for x in content:
                data = x.split("=")
                file_value = data[1]
                if data[1].isdigit():
                    file_value = int(data[1])

                setattr(Config, data[0], file_value)
                print(f"[{count}] Added config = {data[0]} with value = {file_value}\n")
                count += 1

        else:
            print("config.txt file doesn't exist, existing. . .")
            exit(0)

        # set remaining necessary config values
        print(Colors.block + "\nSetting remaining configuration values\n\n" + Colors.reset)
        for attr in dir(Configuration):
            value = getattr(Configuration, attr, None)

            if attr.isupper() and not hasattr(Config, attr):
                setattr(Config, attr, value)
                print(f"[{count}] Added config = {attr} with value = {value}\n")
                count += 1

        clear = input(f"{Colors.block}Should I clear the screen ?{Colors.reset} (Y/N): ")
        if (not clear) or (clear and clear.upper() == "Y"):
            self.clear_screen



if isLocalHost():
    tools = Tools()
    tools.setup_config()
else:
    print("It looks like you deployed this using Docker, Thats why Setting the Non-LocalHost setup ... !")
    for attr in dir(Configuration):
        value = getattr(Configuration, attr, None)
        if attr.isupper() and not hasattr(Config, attr):
            setattr(Config, attr, value)


# default import
from main.userbot import app
bot = app.bot
from main.core.filters import gen
