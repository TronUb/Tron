import os




#todo
if os.uname()[1] == "localhost":
	response = os.system("pip3 install -r requirements.txt")
	if response == 0:
		print("Successfully Installed all requirements")
	else:
		print("Failed to install requirements")




# if you deploy this bot by localhost method, then replace all the necessary part of variables given below after '=' sign with your desired values.
# for example edit like 'API_ID = 1234567' instead of 'API_ID = os.getenv("API_ID")'
# Note: don't touch anything else given below except the values you wanna change otherwise you'll face errors.
#-------------------------------------------------------------------------------------------------------------
class Config(object):
	# api id of your telegram account (required)
	API_ID = os.getenv("API_ID")
	# api hash of your telegram account (required)
	API_HASH = os.getenv("API_HASH")
	# Create a session from session.py (required)
	SESSION = os.getenv("SESSION")
# ------------------
	# temporary download location (required)
	TEMP_DICT = os.getenv("TEMP_DICT", os.path.abspath(".") + "/downloads/")
	# official repo for updates
	UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/beastzx18/Tron.git")
# ------------------
	# heroku api key (required if hosted on heroku)
	HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
	# heroku app name (required if hosted on heroku)
	HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
	# database url (required)
	DB_URI = os.getenv("DATABASE_URL")
# ------------------
	# these users can use your bot / userbot
	SUDO_USERS = os.getenv("SUDO_USERS")
	# a group to store logs, etc (required)
	LOG_CHAT = os.getenv("LOG_CHAT")
	# command handler, if you give ! (exclamation) then you can do like this !ping => pong !
	PREFIX = os.getenv("PREFIX", ".")
	# for more info visit docs.pyrogram.org, workers section (required)
	WORKERS = os.getenv("WORKERS", 8)
	# exclude official plugins from installing
	NO_LOAD = os.getenv("NO_LOAD")
	# default reason for afk plugin
	AFK_TEXT = os.getenv("AFK_TEXT", "I am busy Now !")
# ------------------
	# add True to enable (default: False)
	PMPERMIT = os.getenv("PMPERMIT", False)
	# pmpermit pic 
	PMPERMIT_PIC = os.getenv("PMPERMIT_PIC", False)
	# custom  pmpermit security text (optional)
	PMPERMIT_TEXT = os.getenv("PMPERMIT_TEXT", "Hey ! This is [Tron Userbot](https://t.me/tronuserbot) Security System.\n**You will be blocked if you spammed my owner's pm**\nCurrently My Owner is busy! So Wait Until He Arrives. 👍🏻\nAnd Better Not To Spam His here!")
	# pmpermit warn limit
	PM_LIMIT = os.getenv("PM_LIMIT", 4)
	# this is used in time plugin
	TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
# -------------------
	# your custom name (default: telegram name)
	USER_NAME = os.getenv("USER_NAME")
	# your custom bio (default: None)
	USER_BIO = os.getenv("USER_BIO")
	# used for alive plugin (default: official tronuserbot logo image)
	USER_PIC = os.getenv("USER_PIC", "https://telegra.ph/file/1073e200f9d8e70b91f0d.jpg")
	# add your telegram id if bot fails to get your id 
	USER_ID = os.getenv("USER_ID")
	# add your username if bot fails to get your username
	USER_USERNAME = os.getenv("USER_USERNAME")
# --------------------
	# this bio will be shown in /help menu (default: official bio from bot) 
	BOT_BIO = os.getenv("BOT_BIO")
	# your assistants custom name (default: NORA)
	BOT_NAME = os.getenv("BOT_NAME", "NORA")
	# your assistants alive pic (optional)
	BOT_PIC = os.getenv("BOT_PIC", "https://telegra.ph/file/4d93e5fa480b5e53d898f.jpg")
	# provide this if bot fails to get username of bot (optional)
	BOT_USERNAME = os.getenv("BOT_USERNAME")
	# telegram id of bot if failed to get automatically (optional)
	BOT_ID = os.getenv("BOT_ID")
	# without this the bot will not work (required)
	TOKEN = os.getenv("TOKEN")
# ---------------------
	# thumbnail used while uploading plugins, etc. (optional)
	THUMB_PIC = os.getenv("THUMB_PIC", "material/images/tron.png")
# ---------------------
	# your telegraph account name (default: Tronuserbot)
	TL_NAME = os.getenv("TL_NAME")
	# this will be shown before (as a prefix) the texts in the help dex (default: None)
	HELP_EMOJI = os.getenv("HELP_EMOJI")


