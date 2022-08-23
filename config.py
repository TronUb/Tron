""" Configuration file to get secure data we need """

import os
import platform
import subprocess

        

_PMPERMIT_TEXT = """
Hey ! This is [Tron Userbot](https://t.me/tronuserbot) Security System.
**You will be blocked if you spammed my owner's pm**
Currently My Owner is busy ! So Wait Until He Arrives. 
And Better Not To Spam His here !
"""


# ------------------
class Configuration(object): # pylint: disable=too-few-public-methods
    """ configuration class """
    # api id of your telegram account (required)
    API_ID = os.getenv("API_ID")
    # api hash of your telegram account (required)
    API_HASH = os.getenv("API_HASH")
    # create a session using command [ python3 session.py ] or use repl.it (required)
    SESSION = os.getenv("SESSION")
# ------------------
    # temporary download location (required)
    TEMP_DICT = os.getenv("TEMP_DICT", os.path.abspath(".") + "/downloads/")
    # official repo for updates
    UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/TronUb/Tron.git")
# ------------------
    # heroku api key (required -> if hosted on heroku)
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
    # heroku app name (required -> if hosted on heroku)
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
    # database url (required)
    DB_URI = os.getenv("DATABASE_URL")
# ------------------
    # these users can use your userbot
    SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()] # splits on spaces
    # a group to store logs, etc (required)
    LOG_CHAT = int(os.getenv("LOG_CHAT", "-100"))
    # command trigger, it works like this: .ping => result: pong !
    TRIGGER = os.getenv("TRIGGER", ".")
    # for more info visit docs.pyrogram.org, workers section
    WORKERS = int(os.getenv("WORKERS", "8"))
    # exclude official plugins from installing, give a space between plugin names
    NO_LOAD = [int(x) for x in os.getenv("NO_LOAD", "").split()] # splits on spaces
    # default reason for afk plugin
    AFK_TEXT = os.getenv("AFK_TEXT", "I am busy Right Now !")
# ------------------
    # add True to enable (default: False)
    PMPERMIT = os.getenv("PMPERMIT", None)
    # pmpermit pic (optional)
    PMPERMIT_PIC = os.getenv("PMPERMIT_PIC", "https://telegra.ph/file/eb4d05653b1e6b4798cbb.jpg")
    # custom  pmpermit security text (optional)
    PMPERMIT_TEXT = os.getenv("PMPERMIT_TEXT", _PMPERMIT_TEXT)
    # pmpermit warn limit (optional)
    PM_LIMIT = int(os.getenv("PM_LIMIT", "4"))
    # this is used to get your accurate time
    TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
# -------------------
    # your custom name (default: telegram name)
    USER_NAME = os.getenv("USER_NAME")
    # your custom bio (default: telegram bio)
    USER_BIO = os.getenv("USER_BIO")
    # used for alive plugin (default: tronuserbot logo image)
    USER_PIC = os.getenv("USER_PIC", "https://telegra.ph/file/48f5dc15d51ea7f721275.jpg")
    # add your telegram id if bot fails to get your id
    USER_ID = os.getenv("USER_ID")
    # add your username if bot fails to get your username
    USER_USERNAME = os.getenv("USER_USERNAME")
# --------------------
    # this bio will be shown in '/help' menu (default: official bio from bot)
    BOT_BIO = os.getenv("BOT_BIO")
    # your assistants custom name (default: Nora)
    BOT_NAME = os.getenv("BOT_NAME", "Nora")
    # your assistants alive pic (optional)
    BOT_PIC = os.getenv("BOT_PIC")
    # provide this if bot fails to get username of bot (optional)
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    # telegram id of bot if failed to get automatically (optional)
    BOT_ID = os.getenv("BOT_ID")
    # access token of your bot, without this the bot will not work (required)
    TOKEN = os.getenv("TOKEN")
# ---------------------
    # thumbnail used while uploading plugins, etc. (optional)
    THUMB_PIC = os.getenv("THUMB_PIC", "./main/core/resources/images/tron-square.png")
# ---------------------
    # your telegraph account name (default: Tronuserbot)
    TL_NAME = os.getenv("TL_NAME", "Tron UserBot")
    # this will be shown before (as a prefix) the texts in the help dex (default: None)
    HELP_EMOJI = os.getenv("HELP_EMOJI", "")
# ---------------------
    # spotify token for spotify now
    SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")




def package_installed(package_name: str):
    return (subprocess.run(
        [
            "pip3",
            "show",
            package_name
        ],
        stdout=subprocess.PIPE
    )).stdout.decode()


def requirements():
    with open("requirements.txt", "r") as f:
        return f.read().split("\n")


def requirements_installed():
    filename = "temp.info"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read()

        if content.isdigit() and int(content) == 30: # 30 requirements
            return True

    return None


if platform.uname()[1] in ("localhost"):
    if requirements_installed():
        count = 0
        print("Checking Packages:\n\n")
        for pkg in requirements():
            if not package_installed(pkg.split("=")[0].lower()):
                if pkg: # empty string
                    os.system(f"pip3 install {pkg}")
            else:
                if pkg: # don't count empty string
                    count += 1
            if pkg: # empty string
                print(f"\n{pkg} installed: Yes")

        with open("temp.info", "w") as f:
            f.write(str(count))

    class Config:
        pass

    # check if the user config file exists
    if os.path.exists("config.txt"):
        with open("config.txt") as f:
            content = f.read().split("\n")

        # set text file config values
        for x in content:
            data = x.split("=")
            if data[0] in config_atr:
                setattr(Config, data[0], data[1])

        # set remaining necessary config values
        config_txt = dir(Config)
        for attr in dir(Configuration):
            if attr.isupper() and not attr in config_txt:
                setattr(Config, attr, getattr(Configuration, att, None)

else:
    class Config(Configuration):
        pass

