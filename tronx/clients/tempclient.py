import os
import sys
import platform
import subprocess




if sys.version_info[0] < 3 or sys.version_info[1] < 9:
	""" lower version will produce errors in userbot """
	log.error("python version 3.9.0 or greater is required, bot is quitting !")
	quit(1)


if list(platform.uname())[1] == "localhost":
	counter = 0
	if counter == 0:
		from demo_config import Config
		try:
			# installing these packages using standard method in termux
			os.system("apt update && apt upgrade")
			# install lxml
			one = os.system("pkg install libxml2 clang libxslt")
			two = subprocess.call(["pip3", "install", "lxml"])
			# install psycopg2
			three = os.system("pkg install postgresql python make clang")
			four = subprocess.call(["pip3", "install", "psycopg2"])
			# install remaining requirements
			five = subprocess.call(["pip3", "install", "-r", "requirements.txt"])
			os.system("clear")
			if one + two + three + four + five == 0:
				print("\nSuccessfully installed requirements.\n")
			else:
				print("\nFailed to install some requirements, it might show some errors.\n")
			counter += 1
		except Exception as e:
			print(e)
else:
	from config import Config

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid

from telegraph import Telegraph




if not Config.LOG_CHAT:
	""" log chat is required """
	log.warning("LOG_CHAT is important for bots normal working, please fill it, quitting.")
	quit(1)


if not Config.DB_URI:
	""" database is required """
	log.warning("DB_URI is important please fill this requirement, quitting.")
	quit(1)





class Initialisation(Collector):
	"""tempclients initialisation"""
	# clients
	tempapp = Client(session_name=Config.SESSION, api_id=Config.API_ID, api_hash=Config.API_HASH)
	tempbot = Client(session_name=Config.SESSION, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.TOKEN)
	# start
	tempapp.start()
	tempbot.start()
	# app
	appdata = tempapp.get_me()
	USER_DC = appdata.dc_id
	USER_ID = appdata.id
	USER_NAME = appdata.first_name
	USER_USERNAME = f"@{appdata.username}" if appdata.username is not None else ""
	# bot
	botdata = tempbot.get_me()
	BOT_DC = botdata.dc_id
	BOT_ID = botdata.id
	BOT_NAME = botdata.first_name
	BOT_USERNAME = f"@{botdata.username}" 
	# stop
	tempapp.stop()
	tempbot.stop()
