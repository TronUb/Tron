""" everything starts here """

import os
import socket
import platform
import subprocess
import pkg_resources
from main.others import Colors
from config import Configuration




class Config:
    pass


def isLocalHost():
    return os.path.exists("./config.txt")


class Tools:
    device = platform.uname()[0].lower()
    is_linux = (device=="linux")
    is_windows = (device=="windows")

    @property
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
                if pkg.startswith("git+https://github.com/"):
                    os.system(f"python -m pip install {pkg}")
                else:
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
        self.clear_screen

        # check requirements & install
        self.check_requirements()
        self.clear_screen

        # check if the user config file exists
        if os.path.exists("config.txt"):
            print("config.txt file exists: Yes\n\n")
            with open("config.txt") as f:
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



tools = Tools()

if(isLocalHost()):
    tools.setup_config()
else:
    print("Setting the Non-LocalHost setup ... !")
    for attr in dir(Configuration):
        value = getattr(Configuration, attr, None)
        if attr.isupper() and not hasattr(Config, attr):
            setattr(Config, attr, value)


# default import
from main.userbot import app
bot = app.bot
from main.core.filters import gen
