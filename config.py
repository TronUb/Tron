""" Configuration file to get secure data we need """

import os


_PMPERMIT_TEXT = """
Hey ! This is [Tron Userbot](https://t.me/tronuserbot) Security System.
**You will be blocked if you spammed my owner's pm**
Currently My Owner is busy ! So Wait Until He Arrives.
And Better Not To Spam His here !
"""


# ------------------
class Configuration: # pylint: disable=too-few-public-methods
    """ configuration class """

# ---- important ----
    # api id of your telegram account (required)
    API_ID = os.getenv("API_ID")
    # api hash of your telegram account (required)
    API_HASH = os.getenv("API_HASH")
    # create a session using command [ python3 session.py ] or use repl.it (required)
    SESSION = os.getenv("SESSION")
    # access token of your bot, without this the bot will not work (required)
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    # database url (required)
    DB_URI = os.getenv("DATABASE_URL", "sqlite:///tron.db")
    # a group to store logs, etc (required)
    LOG_CHAT = int(os.getenv("LOG_CHAT", "-100"))

# ---- heroku ----
    # heroku api key (required -> if hosted on heroku)
    HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
    # heroku app name (required -> if hosted on heroku)
    HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

# ---- afk ----
    # default reason for afk plugin (optional)
    AFK_TEXT = os.getenv("AFK_TEXT", "I am busy Right Now !")

# ---- pmpermit ----
    # add True to enable pmpermit (optional)
    PMPERMIT = os.getenv("PMPERMIT", None)
    # add custom pmpermit pic (optional)
    PMPERMIT_PIC = os.getenv("PMPERMIT_PIC", "https://telegra.ph/file/eb4d05653b1e6b4798cbb.jpg")
    # add custom pmpermit warn text (optional)
    PMPERMIT_TEXT = os.getenv("PMPERMIT_TEXT", _PMPERMIT_TEXT)
    # add custom pmpermit warn limit (optional)
    PM_LIMIT = int(os.getenv("PM_LIMIT", "4"))

# ---- user ----
    # your custom name (default: telegram name)
    USER_NAME = os.getenv("USER_NAME")
    # your custom bio (default: telegram bio)
    USER_BIO = os.getenv("USER_BIO")
    # used for alive plugin (default: tronuserbot logo image)
    USER_PIC = os.getenv("USER_PIC", "https://telegra.ph/file/48f5dc15d51ea7f721275.jpg")
    # add your telegram id if userbot fails to get your user id
    USER_ID = os.getenv("USER_ID")
    # add your username if userbot fails to get your username
    USER_USERNAME = os.getenv("USER_USERNAME")

# --- bot ----
    # provide this if bot failes to get (optional)
    BOT_BIO = os.getenv("BOT_BIO")
    # provide this if bot fails to get (optional)
    BOT_NAME = os.getenv("BOT_NAME", "Nora")
    # provide this if bot fails to get (optional)
    BOT_PIC = os.getenv("BOT_PIC")
    # provide this if bot fails to get (optional)
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    # provide this if bot fails to get (optional)
    BOT_ID = os.getenv("BOT_ID")

# ---- help menu ----
    # this will be shown on 4 buttons (settings, plugins, extra, stats) as prefix and suffix
    HELP_EMOJI = os.getenv("HELP_EMOJI", "")
    # set this text to show on help menu's closed tab
    HELP_TEXT = os.getenv("HELP_TEXT", "")
    # set this to change help menu's default pic
    HELP_PIC = os.getenv("HELP_PIC", "")

# ---- spotify ----
    # spotify token for spotify now
    SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")

# ---- assistant ----
    # set your assistant name, will be used in assistant tab's about section
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Lara")
    # set your assistant age
    ASSISTANT_AGE = os.getenv("ASSISTANT_AGE", "20")
    # set your assistant pic
    ASSISTANT_PIC = os.getenv("ASSISTANT_PIC", "./main/core/resources/images/nora.png")
    # set your assistant about text
    ASSISTANT_TEXT = os.getenv("ASSISTANT_TEXT", "")

# ---- vcbot ----
    # start the vcbot client
    VCBOT = os.getenv("VCBOT", None)
    # make vcbot public so that everyone can use
    VCBOT_ACCESS = os.getenv("VCBOT_ACCESS", None)

# ---- other ----
    # your telegraph account name (default: Tronuserbot)
    TL_NAME = os.getenv("TL_NAME", "Tron UserBot")
    # thumbnail used while uploading plugins, etc. (optional)
    THUMB_PIC = os.getenv("THUMB_PIC", "./main/core/resources/images/tron-square.png")
    # temporary download location (required)
    TEMP_DICT = os.getenv("TEMP_DICT", os.path.abspath(".") + "/downloads/")
    # official repo for updates
    UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/TronUb/Tron.git")
    # this is used to get your accurate time
    TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
    # toggle this on/off to give/remove access of bot to sudo users
    SUDO_ACCESS = os.getenv("SUDO_ACCESS", None)
    # these users can use your userbot
    SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()] # splits on spaces
    # default sudo commands to add in database when adding a sudo
    SUDO_CMDS = [x for x in os.getenv("SUDO_CMDS", "").split()] # splits on spaces
    # command trigger, it works like this: .ping => result: pong !
    TRIGGER = os.getenv("TRIGGER", ".")
    # for more info visit docs.pyrogram.org, workers section
    WORKERS = int(os.getenv("WORKERS", "8"))
    # exclude official plugins from installing, give a space between plugin names
    NO_LOAD = [int(x) for x in os.getenv("NO_LOAD", "").split()] # splits on spaces


