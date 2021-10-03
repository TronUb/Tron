import os




# if you have hosted tron on termux.
# fill your all details here.

#-------------------------------------------------------------------------------------------------------------
class Config(object):
	# required
	API_ID = 
	# required
	API_HASH = ""
	# access Session from your account
	SESSION = ""
# ------------------
	# to download files
	TEMP_DICT = os.path.abspath(".") + "/downloads/"
	# official repo for updates
	UPSTREAM_REPO = "https://github.com/beastzx18/Tron.git"
# ------------------
	# heroku api key 
	HEROKU_API_KEY = ""
	# heroku app name
	HEROKU_APP_NAME = ""
	# database url
	DB_URI = ""
# ------------------
	# log mentioned and other messages
	LOG_CHAT = ""
	 # Insert command prefix, if you insert "!" then you can do !ping
	PREFIX = "."
	# must be int (number)
	WORKERS = 8
	# not loaded or not installed plugins
	NO_LOAD = ""
	# default reason for afk
	AFK_TEXT = "I am busy Now !"
# ------------------
	# add True to enable (default: False)
	PMPERMIT = False
	# pmpermit pic 
	PMPERMIT_PIC = False
	# custom  pmpermit security text (optional)
	PMPERMIT_TEXT = "Hey ! This is [Tron Userbot](https://t.me/tronuserbot) Security System.\n**You will be blocked if you spammed my owner's pm**\nCurrently My Owner is busy! So Wait Until He Arrives. 👍🏻\nAnd Better Not To Spam His here!"
	# pmpermit warn limit
	PM_LIMIT = 4
	# add your city time zone
	TIME_ZONE = "Asia/Kolkata"
# -------------------
	# for time plugin (default : Asia/Kolkata)
	USER_NAME = ""
	# for alive plugin (optional)
	USER_BIO = ""
	# for alive plugin (optional)
	USER_PIC = "https://telegra.ph/file/1073e200f9d8e70b91f0d.jpg"
# --------------------
	# your custom bot bio (optional)
	BOT_BIO = ""
	# your assistants custom name (default: LARA)
	BOT_NAME = "LARA"
	# your aassistants alive pic (optional)
	BOT_PIC = "https://telegra.ph/file/4d93e5fa480b5e53d898f.jpg"
	# bot username for bot
	BOT_USERNAME = None
	# token of your bot if you want to use assistant
	TOKEN = ""
# ---------------------
	THUMB_PIC = "material/images/tron.png"
	# sudo users can use your bot too
	SUDO_USERS = []



class Production(Config):
	LOGGER = False

# ----------------------
class Development(Config):
	LOGGER = True
