import os



termux = object
if os.uname()[1] == "localhost":
	from termux import Termuxconfig
	inside = Termuxconfig
	


# if you deployed this userbot using localhost method, then replace all the necessary parts of the variables given below after '=' sign with the required values.
# for example edit like 'API_ID = 1234567' instead of 'API_ID = os.getenv("API_ID")'
# Warning: don't touch anything else given below except the values you wanna change otherwise you'll get errors.
#-------------------------------------------------------------------------------------------------------------
class Config(inside):
	""" configuration class """
	if not termux:
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
	if not termux:
		# database url (required)
		DB_URI = os.getenv("DATABASE_URL")
# ------------------
	# these users can use your userbot
	SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split()] # splits on spaces
	if not termux:
		# a group to store logs, etc (required)
		LOG_CHAT = int(os.getenv("LOG_CHAT"))
	# command handler, if you give (exclamation symbol = !) then you can do like this command: !ping => result: pong !
	PREFIX = os.getenv("TRIGGER", ".")
	# for more info visit docs.pyrogram.org, workers section
	WORKERS = int(os.getenv("WORKERS", 8))
	# exclude official plugins from installing, give a space between plugin names
	NO_LOAD = [int(x) for x in os.getenv("NO_LOAD", "").split()] # splits on spaces
	# default reason for afk plugin
	AFK_TEXT = os.getenv("AFK_TEXT", "I am busy Now !")
# ------------------
	# add True to enable (default: False)
	PMPERMIT = os.getenv("PMPERMIT", False)
	# pmpermit pic (optional)
	PMPERMIT_PIC = os.getenv("PMPERMIT_PIC")
	# custom  pmpermit security text (optional)
	PMPERMIT_TEXT = os.getenv("PMPERMIT_TEXT", "Hey ! This is [Tron Userbot](https://t.me/tronuserbot) Security System.\n**You will be blocked if you spammed my owner's pm**\nCurrently My Owner is busy! So Wait Until He Arrives. 👍🏻\nAnd Better Not To Spam His here!")
	# pmpermit warn limit (optional)
	PM_LIMIT = int(os.getenv("PM_LIMIT", 4))
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
	# your assistants custom name (default: NORA)
	BOT_NAME = os.getenv("BOT_NAME", "NORA")
	# your assistants alive pic (optional)
	BOT_PIC = os.getenv("BOT_PIC", "https://telegra.ph/file/48f5dc15d51ea7f721275.jpg")
	# provide this if bot fails to get username of bot (optional)
	BOT_USERNAME = os.getenv("BOT_USERNAME")
	# telegram id of bot if failed to get automatically (optional)
	BOT_ID = os.getenv("BOT_ID")
	if not termux:
		# access token of your bot, without this the bot will not work (required)
		TOKEN = os.getenv("TOKEN")
# ---------------------
	# thumbnail used while uploading plugins, etc. (optional)
	THUMB_PIC = os.getenv("THUMB_PIC", "material/images/tron.png")
# ---------------------
	# your telegraph account name (default: Tronuserbot)
	TL_NAME = os.getenv("TL_NAME")
	# this will be shown before (as a prefix) the texts in the help dex (default: None)
	HELP_EMOJI = os.getenv("HELP_EMOJI")


