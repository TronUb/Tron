import os
import sys
import time
import platform
import logging
import subprocess
import importlib
from typing import Union, List




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

import pyrogram
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from telegraph import Telegraph
from tronx.methods import Methods




if not Config.LOG_CHAT:
	""" log chat is required """
	log.warning("LOG_CHAT is important for bots normal working, please fill it, quitting.")
	quit(1)


if not Config.DB_URI:
	""" database is required """
	log.warning("DB_URI is important please fill this requirement, quitting.")
	quit(1)




class Collector(Methods, Config):
	# versions /

	userbot_version = "v.0.0.5"
	assistant_version = "v.0.0.1"
	python_version = str(platform.python_version())
	pyrogram_version = str(pyrogram.__version__)

	# database /

	db_status = "Available" if Config.DB_URI else "Not Available"

	# containers /

	CMD_HELP = {}
	HELP = {}

	# owner details /

	OWNER_NAME = "࿇•ẞᗴᗩSԵ•࿇"
	OWNER_ID = 1790546938
	OWNER_USERNAME = "@BEASTZX"

	# other /

	Repo = "https://github.com/beastzx18/Tron"
	StartTime = time.time()

	# debugging /

	logging.basicConfig(level=logging.WARNING)
	log = logging.getLogger(__name__)

	# telegraph /

	telegraph = Telegraph()
	telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")





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





class utils(Initialisation):
	def clear():
		""" clear terminal logs """
		subprocess.call("clear" if os.name == "posix" else "cls") 


	def add_user(self, user_id: Union[int, List[int]], chat_id: str):
		""" Add users in groups / channels """
		try:
			done = app.add_chat_members(chat_id, user_id)
			return True if done else False
		except Exception as e:
			print(e)


	def exists(self, user_id: int, chat_id: str):
		for x in app.iter_chat_members(chat_id):
			if x.user.id == user_id:
				return True
		

	def check_bot_in_log_chat(self):
		try:
			if bot:
				print("Checking presence of bot in log chat . . .\n")
				try:
					if self.exists(BOT_ID, LOG_CHAT) is False:
						self.add_user(self.LOG_CHAT, self.BOT_ID)
						print(f"Added bot in log chat . . .\n")
					else:
						print(f"Bot is already present in log chat . . .\n")
				except PeerIdInvalid:
					print("Peer id is invalid, Manually send a message in log chat . . .\n")

			else:
				self.log.warning("Bot is not available, please check (TOKEN, API_ID, API_HASH)")
		except Exception as e:
			print(e)


	def get_readable_time(seconds: int) -> str:
		count = 0
		ping_time = ""
		time_list = []
		time_suffix_list = ["s", "m", "h", "days"]

		while count < 4:
			count += 1
			remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
			if seconds == 0 and remainder == 0:
				break
			time_list.append(int(result))
		seconds = int(remainder)

		for x in range(len(time_list)):
			time_list[x] = str(time_list[x]) + time_suffix_list[x]
		if len(time_list) == 4:
			ping_time += time_list.pop() + ", "

		time_list.reverse()
		ping_time += ":".join(time_list)

		return ping_time


	def uptime(self):
		""" Bot active time """
		return self.get_readable_time(time.time() - self.StartTime)


	def import_module(self, path, exclude=[], display_module=True):
		"""Modified version of pyrogram smart plugins"""
		bin = []
		bin.clear()

		if not os.path.exists(path):
			return print(f"No path found: {path}")

		plugins = []
		for x in os.listdir(path):
			if x.endswith(".py"):
				if not x in ["__pycache__",  "__init__.py"]:
					plugins.append(x.replace(".py", ""))

		py_path_raw = ".".join(path.split("/"))
		py_path = py_path_raw[0:len(py_path_raw)-1]

		count = 0
		for x in plugins:
			if not x in exclude:
				importlib.import_module(py_path + "." + x)
				count += 1
				bin.append(x)

		if display_module:
			data = sorted(bin)
			for x in data:
				print(x + " Loaded !")
		return count

