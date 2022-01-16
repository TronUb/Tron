import os
import sys
import time
import logging
import platform
import subprocess

from typing import Union, List
from tronx.methods import Methods




# debugging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)



if sys.version_info[0] < 3 or sys.version_info[1] < 9:
	""" lower version will produce errors in userbot """
	log.error("python version 3.9.0 or greater is required, bot is quitting !")
	quit(1)




# termux requirement installation
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




if not Config.LOG_CHAT:
	""" log chat is required """
	log.warning("LOG_CHAT is important for bots normal working, please fill it, quitting.")
	quit(1)




if not Config.DB_URI:
	""" database is required """
	log.warning("DB_URI is important please fill this requirement, quitting.")
	quit(1)




if not os.path.exists("downloads"):
	""" all files are downloaded here """
	os.mkdir("downloads")



# temporary clients
app = Client(
	session_name=Config.SESSION,
	api_id=Config.API_ID,
	api_hash=Config.API_HASH,
	workers=Config.WORKERS,
)




bot = Client(
	session_name="lara",
	api_id=Config.API_ID,
	api_hash=Config.API_HASH,
	bot_token=Config.TOKEN,
)



# Things don't work properly without this
if app:
	app.start()
	data = app.get_me()
	USER_ID = data.id
	USER_NAME = data.first_name
	USER_USERNAME = f"@{data.username}" if data.username else "None"
	USER_DC = data.dc_id
	telegraph = Telegraph()
	telegraph.create_account(short_name=USER_NAME if USER_NAME else "Tron userbot")
	app.stop()




if bot:
	bot.start()
	data = bot.get_me()
	BOT_ID = data.id
	BOT_NAME = data.first_name
	BOT_USERNAME = f"@{data.username}"
	BOT_DC = data.dc_id
	bot.stop()




def clear():
	""" clear terminal logs """
	subprocess.call("clear" if os.name == "posix" else "cls") 




def add_user(user_id: Union[int, List[int]], chat_id: str):
	""" Add users in groups / channels """
	try:
		done = app.add_chat_members(
			chat_id, 
			user_id
			)
		return True if done else False
	except Exception as e:
		print(e)




# check if the bot is in log chat 
def exists(user_id: int, chat_id: str):
	_data = []
	_data.clear()
	lime = app.get_chat_members(chat_id)

	for x in lime:
		_data.append(x.user.id)
	return True if user_id in _data else False




def check_bot_in_log_chat():
	try:
		if bot:
			print("Checking presence of bot in log chat . . .\n")
			try:
				if exists(BOT_ID, LOG_CHAT) is False:
					add_user(
						LOG_CHAT,
						BOT_ID
					)
					print(f"Added bot in log chat . . .\n")
				else:
					print(f"Bot is present in log chat . . .\n")
			except PeerIdInvalid:
				print("Peer id is invalid, Manually send a message in log chat . . .\n")
				pass
		else:
			log.warning("Bot is not available, please check (TOKEN, API_ID, API_HASH)")
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




def uptime():
	""" Bot active time """
	return get_readable_time(time.time() - StartTime)




# telegraph plugin
telegraph = Telegraph()
telegraph.create_account(short_name=USER_NAME if USER_NAME else "Tron userbot")




class Inversion(object):
	global userbot_version, assistant_version, python_version, pyrogram_version, DB_URI, db_status, StartTime, REPO, LOG_CHAT, PREFIX, SESSION, TOKEN, API_ID, API_HASH, WORKERS, USER_BIO, OWNER_NAME, OWNER_ID, OWNER_USERNAME 
	# versions /

	userbot_version = "v.0.0.5"
	assistant_version = "v.0.0.1"
	python_version = str(platform.python_version())
	pyrogram_version = str(pyrogram.__version__)

	# database /

	DB_URI = Config.DB_URI
	db_status = "Available" if DB_URI else "Not Available"

	# containers
	CMD_HELP = {}
	HELP = {}

	# configurations shortcut /

	LOG_CHAT = Config.LOG_CHAT
	PREFIX = Config.PREFIX
	SESSION = Config.SESSION
	TOKEN = Config.TOKEN
	API_ID = Config.API_ID
	API_HASH = Config.API_HASH
	WORKERS = Config.WORKERS
	USER_BIO = Config.USER_BIO

	# owner details /

	OWNER_NAME = "࿇•ẞᗴᗩSԵ•࿇"
	OWNER_ID = 1790546938
	OWNER_USERNAME = "@BEASTZX"

	# other /

	REPO = "https://github.com/beastzx18/Tron"
	StartTime = time.time()




# main client classes
class tron(Client, Methods, Inversion):
	""" Userbot """
	def __init__(self):
		super().__init__(
		session_name=Config.SESSION,
		api_id=Config.API_ID,
		api_hash=Config.API_HASH,
		workers=Config.WORKERS,
		)
        



class lara(Client):
	""" Assistant """
	def __init__(self):
		super().__init__(
		session_name="lara",
		api_id=Config.API_ID,
		api_hash=Config.API_HASH,
		bot_token=Config.TOKEN,
		)




# instances of pyrogram.Client()
app = tron() if SESSION else False
bot = lara() if TOKEN else False







