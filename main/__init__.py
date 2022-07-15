""" this file determines deployment method """

import os
import sys
import platform
import subprocess
from time import sleep
import pkg_resources



dependencies = "Pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir Pillow bs4 covid pySmartDL pyDownload SQLAlchemy==1.3.23 TgCrypto httpx pytz py-postgresql psycopg2 CurrencyConverter deep-translator gTTS git-python Wikipedia-API speedtest-cli==2.1.3 qrcode bing-image-downloader pysimplelog" 


# run shell commands
def shell(args: str):
    return subprocess.run(args.split(), capture_output=True).stdout.decode("ascii")


# clear screen
def clear():
    return os.system("clear")


# upgrade linux packages
def update_upgrade(msg: str, clear_screen: bool=True):
    clear()
    print(msg + "\n\n")
    os.system("apt update")
    os.system("apt upgrade")
    if clear_screen:
        clear()
    return True


# check & install python if not installed
def check_python(msg: str):
    print(msg + "\n\n")
    output = shell("python3 -V")
    if "No command python3 found" in output:
        print("Python is not installed: installing . . .\n\n")
        os.system("apt install python3")
        clear()
    else:
        print("Python is already installed.")
        sleep(1)
        clear()


# install wheel 
def install_wheel():
    os.system("pip3 install wheel")
    clear()
    


# install requirements 
def install_requirements():
    update_upgrade("Updating and upgrading ...")
    check_python("Checking python . . .")
    install_wheel()

    for x in dependencies.split():
        installed_packages = [p.project_name for p in pkg_resources.working_set]
        pkg = x.split("=")[0]

        if not pkg in installed_packages:
            if pkg == "Pillow":
                print(f"\nInstalling package {x}\n\n")
                os.system("pkg install libjpeg-turbo")
                os.system("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/'")
                os.system("pip3 install Pillow")
                clear()
                continue

            print(f"\nInstalling package {x}\n\n")
            os.system(f"pip3 install {x}")
            clear()
    clear()
    return True


def create_termuxconfig():
    ATTR = ("API_ID", "API_HASH", "SESSION", "DB_URI", "LOG_CHAT", "TOKEN")
    file = open("termuxconfig.py", "w+")
    file.write("class TermuxConfig:\n\ttemp = 'value'\n")
    for x in ATTR:
        if x == "DB_URI":
            continue
            data = input(f"\nEnter your {x}: ")
            value = int(data) if data and data == "LOG_CHAT" else f"'{data}'"

        file.write(f"""\t{x.replace('"', "")} = {value}\n""")
    file.close()



# --- begin ---

install_requirements()

if shell("uname -n") in ("localhost"):
    try:
        from termuxconfig import TermuxConfig
    except (ImportError, ModuleNotFoundError):
        create_termuxconfig()
        from termuxconfig import TermuxConfig     


from main.userbot.client import app
bot = app.bot
from main.core.filters import gen, regex
