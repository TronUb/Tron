import os




#-------------------------------------------------------------------------------------------------------------
class Config(object):
	# required
	API_ID = os.getenv("API_ID")
	# required
	API_HASH = os.getenv("API_HASH")
	# access Session from your account
	SESSION = os.getenv("SESSION")
# ------------------
	# to download files
	TEMP_DICT = os.getenv("TEMP_DICT", os.path.abspath(".") + "/downloads/")
	# official repo for updates
	UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/beastzx18/Tron.git")
# ------------------
	# heroku api key 
	HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")
	# heroku app name
	HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
	# database url
	DB_URI = os.getenv("DATABASE_URL")
# ------------------
	# sudo users can user your bot too
	SUDO_USERS = os.getenv("SUDO_USERS")
	# log mentioned and other messages
	LOG_CHAT = os.getenv("LOG_CHAT")
	 # Insert command prefix, if you insert "!" then you can do !ping
	PREFIX = os.getenv("PREFIX", ".")
	# must be int (number)
	WORKERS = os.getenv("WORKERS", 8)
	# not loaded or not installed plugins
	NO_LOAD = os.getenv("NO_LOAD")
	# default reason for afk
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
	# add your city time zone
	TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Kolkata")
# -------------------
	# for time plugin (default : Asia/Kolkata)
	USER_NAME = os.getenv("USER_NAME")
	# for alive plugin (optional)
	USER_BIO = os.getenv("USER_BIO")
	# for alive plugin (optional)
	USER_PIC = os.getenv("USER_PIC", "https://telegra.ph/file/1073e200f9d8e70b91f0d.jpg")
	# add your id if bot fails to get your id
	USER_ID = os.getenv("USER_ID")
	# add your username if bot fails to get your username
	USER_USERNAME = os.getenv("USER_USERNAME")
# --------------------
	# your custom bot bio (optional)
	BOT_BIO = os.getenv("BOT_BIO")
	# your assistants custom name (default: LARA)
	BOT_NAME = os.getenv("BOT_NAME", "LARA")
	# your aassistants alive pic (optional)
	BOT_PIC = os.getenv("BOT_PIC", "https://telegra.ph/file/4d93e5fa480b5e53d898f.jpg")
	# bot username for bot
	BOT_USERNAME = os.getenv("BOT_USERNAME")
	# token of your bot if you want to use assistant
	TOKEN = os.getenv("TOKEN")
# ---------------------
	THUMB_PIC = os.getenv("THUMB_PIC", "material/images/tron.png")



