""" everything starts here """

import re
import os
import json
import socket
import platform
import subprocess
import pkg_resources
from main.colors import Colors
from config import Configuration
from string import punctuation as special_characters





symbols = re.compile(f"[{special_characters}]")

class Config:
    pass


class HostType:
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    localhost_hostname = "localhost"
    localhost_ip_address = "127.0.0.1"
    is_localhost = (hostname==localhost_hostname) and (ip_address==localhost_ip_address) 


class Tools:
    device = platform.uname()[0].lower()
    is_linux = (device=="linux")
    is_windows = (device=="windows")

    def clear_screen(self):
        os.system("clear" if self.is_linux else "cls")

    def check_command(self, args: list):
        return (subprocess.run(
            args,
            stdout=subprocess.PIPE,
            shell=True
        )).stdout.decode()


    def requirements(self):
        with open("requirements.txt", "r") as f:
            return [x for x in f.read().split("\n") if x not in ("\n", "")]


    def check_requirements(self):
        self.install_ffmpeg()
        print("Checking Packages:\n\n")
        for pkg in self.requirements():
            try:
                pkg_resources.require([pkg])
            except pkg_resources.DistributionNotFound as e:
                print(f"\nSince {e.req} is not Installed, Installing {e.req}")
                if e.req == "numpy":
                    self.install_numpy()

                elif e.req == "lxml":
                    self.install_lxml()

                elif e.req == "psycopg2":
                    self.install_psycopg2()

                elif e.req == "pillow":
                    self. install_pillow()

                else:
                    os.system(f"python -m pip install {e.req}")


    def install_numpy(self):
        print("\nInstalling numpy . . .\n")
        os.system('MATHLIB="m" python -m pip install numpy')


    def install_lxml(self):
        if self.is_windows:
            os.system("scoop install libxml2")
            os.system("scoop install libxslt")
        else:
            os.system("apt install libxml2 libxslt")
        print("\nInstalling lxml . . .\n")
        os.system("python -m pip install lxml")


    def install_psycopg2(self):
        if self.is_windows:
            os.system("scoop install postgresql python make clang")
        else:
            os.system("apt install postgresql python make clang")
        print("\nInstalling psycopg2 . . .\n")
        os.system("python -m pip install psycopg2")


    def install_pillow(self):
        if self.windows:
            os.system("scoop install libjpeg-turbo")
            os.system('./configure CFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib"')
        else:
            os.system("apt install libjpeg-turbo")
            os.system('LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/"')
        print("\nInstalling pillow . . .")
        os.system("python -m pip install pillow")

    def install_ffmpeg(self):
        if tools.is_windows:
            # install ffmpeg

            # permission needed in windows
            os.system('Set-ExecutionPolicy RemoteSigned -Scope CurrentUser')
            # install scoop for installing scoop & other packages
            os.system('Invoke-Expression "& {$(Invoke-RestMethod get.scoop.sh)} -RunAsAdmin"')
            # install ffmpeg through scoop
            os.system('scoop install ffmpeg')

        elif tools.is_linux:
            # install ffmpeg

            os.system('apt install ffmpeg')

        else:
            print('\nUnknown device, Existing . . .')
            exit(0)

    def setup_config(self):
        count = 1
        self.clear_screen()

        # check requirements & install
        self.check_requirements()
        self.clear_screen()

        # check if the user config file exists
        if os.path.exists("config.text"):
            print("config.text file exists: Yes\n\n")
            with open("config.text") as f:
                content = [x for x in f.read().split("\n") if x not in ("\n", "")]

            # set text file config values
            print(Colors.block + "Setting configuration values.\n\n" + Colors.reset)
            for string in content:
                key, value = string.split("=")

                if value.isdigit():
                    # convert str into int
                    value = int(value)
                elif value.isalnum() or symbols.search(value):
                    # not needed but don't pass an alphanumeric to json.loads()
                    value = str(value)
                else:
                    # load string lists as lists
                    value = json.loads(value)

                setattr(Config, key, value)
                print(f"[{count}] Added config = {key} with value = {value}\n")
                count += 1

        else:
            print("config.text file doesn't exist, existing. . .")
            exit(0)

        # set remaining necessary config values
        print(Colors.block + "\nSetting remaining configuration values\n\n" + Colors.reset)
        for attr in dir(Configuration):
            value = getattr(Configuration, attr, None)

            if attr.isupper() and not hasattr(Config, attr):
                setattr(Config, attr, value)
                print(f"[{count}] Added config = {attr} with value = {value}\n")
                count += 1

        clear = input(f"{Colors.block}Should we clear screen ?{Colors.reset} (Y/N): ")
        if (not clear) or (clear and clear.upper() == "Y"):
            self.clear_screen()



tools = Tools()
hosttype = HostType()


if hosttype.is_localhost:
    # start setup
    tools.setup_config()


# don't change this
# default import
from main.userbot.client import app
bot = app.bot
from main.core.filters import gen, regex
