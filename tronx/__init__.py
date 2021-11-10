import os
import sys
import time
import logging
import asyncio
import platform
import subprocess

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.filters import Filter
from pyrogram.errors import PeerIdInvalid

from typing import Union, List

from telegraph import Telegraph




# debugging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)




# termux requirement installation
if list(platform.uname())[1] == "localhost":
	from demo_config import Config
	try:
		# installing these packages using standard method in termux
		# install pillow
		os.system("apt update && apt upgrade")
		one = os.system("pkg install python libjpeg-turbo libcrypt ndk-sysroot clang zlib git")
		two = subprocess.call(["pip3", "install", "pillow"])
		# install lxml
		three = os.system("pkg install libxml2 clang libxslt")
		four = subprocess.call(["pip3", "install", "lxml"])
		# install psycopg2
		five = os.system("pkg install postgresql python make clang")
		six = subprocess.call(["pip3", "install", "psycopg2"])
		# install remaining requirements
		seven = subprocess.call(["pip3", "install", "-r", "requirements.txt"])
		os.system("clear")
		if one + two + three + four + five + six + seven == 0:
			print("\nSuccessfully installed requirements.\n")
		else:
			print("\nFailed to install some requirements, it might show some errors.\n")
	except Exception as e:
		print(e)
else:
	from config import Config




# variables
PREFIX = Config.PREFIX

API_ID = Config.API_ID

API_HASH = Config.API_HASH

SESSION = Config.SESSION

LOG_CHAT = Config.LOG_CHAT

DB_URI = Config.DB_URI

TOKEN = Config.TOKEN

WORKERS = Config.WORKERS

# -x -x -x -x

OWNER_NAME = "࿇•ẞᗴᗩSԵ•࿇"

OWNER_ID = 1790546938

OWNER_USERNAME = "@BEASTZX"

version = "v.0.0.4"

lara_version = "v.0.0.1"

CMD_HELP = {}

HELP = {}

REPO = "https://github.com/beastzx18/Tron"

StartTime = time.time()

__python_version__ = f"{platform.python_version()}"

db_status = "Available" if DB_URI else "Not Available"




if sys.version_info[0] < 3 or sys.version_info[1] < 9:
	""" lower version will produce errors in userbot """
	log.error("python version 3.9.0 or greater is required, bot is quitting !")
	quit(1)




if not LOG_CHAT:
	""" log chat is required """
	log.warning("LOG_CHAT is important for bots normal working, please fill it, quitting.")
	quit(1)




if not DB_URI:
	""" database is required """
	log.warning("DB_URI is important please fill this requirement, quitting.")
	quit(1)




if not os.path.exists("downloads"):
	""" all files are downloaded here """
	os.mkdir("downloads")




def clear():
	""" clear terminal logs """
	subprocess.call("clear" if os.name == "posix" else "cls") 




def get_readable_time(seconds: int) -> str:
	""" seconds to readable time """
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
	ping_time += " : ".join(time_list)

	return ping_time




async def get_self():
	""" Get self information for later use """
	global USER_ID, USER_NAME, USER_USERNAME
	
	USER_ID = None
	USER_DC = None
	USER_NAME = None
	USER_USERNAME = None

	getself = await app.get_me()
	if getself:
		if getself.last_name and getself.username:
			# sometimes users don't have the last name & username
			USER_NAME = f"{getself.first_name} {getself.last_name}"
			USER_USERNAME = f"@{getself.username}"
		else:
			USER_NAME = getself.first_name
			USER_USERNAME = "No Username"
		USER_ID = getself.id
		USER_DC = getself.dc_id
	else:
		log.warning("Failed to get user information (USER_ID, USER_DC, USER_NAME, USER_USERNAME)")  

	return (
		{
			"USER_ID" : USER_ID, 
			"USER_DC" : USER_DC,
			"USER_NAME" : USER_NAME, 
			"USER_USERNAME" : USER_USERNAME
		}
		)




async def get_bot():
	""" Get bot information for later use """
	global BOT_ID, BOT_DC, BOT_NAME, BOT_USERNAME
	
	BOT_ID = None
	BOT_DC = None
	BOT_NAME = None
	BOT_USERNAME = None
	
	getbot = await bot.get_me()
	if getbot:
		# bot have all permanent information
		BOT_ID = getbot.id
		BOT_DC = getbot.dc_id
		BOT_NAME = getbot.first_name
		BOT_USERNAME = "@" + getbot.username
	else:
		log.warning("Failed to get bot information (BOT_ID, BOT_DC, BOT_NAME, BOT_USERNAME)") 
		
	return (
		{
			"BOT_ID" : BOT_ID, 
			"BOT_DC" : BOT_DC, 
			"BOT_NAME" : BOT_NAME, 
			"BOT_USERNAME" : BOT_USERNAME
		}
		)




async def add_user(user_id: Union[int, List[int]], chat_id: str):
	""" Add users in groups / channels """
	try:
		done = await app.add_chat_members(
			chat_id, 
			user_id
			)
		return True if done else False
	except Exception as e:
		print(e)




# check if the bot is in log chat 
async def exists(user_id: int, chat_id: str):
	_data = []
	_data.clear()
	lime = await app.get_chat_members(chat_id)

	for x in lime:
		_data.append(x.user.id)
	return True if user_id in _data else False




async def userlise():
	global telegraph
	try:
		if app:
			await app.start()
			await get_self()
			# telegraph account
			telegraph = Telegraph()
			telegraph.create_account(short_name=USER_NAME if USER_NAME else "Tron userbot") 
			await botlise()
			await app.stop()
		else:
			log.warning("App client is not available, please check your (SESSION, API_ID, API_HASH)")
	except Exception as e:
		print(e)




async def botlise():
	try:
		if bot:
			await bot.start()
			await get_bot()
			print("Checking presence of bot in log chat . . .\n")
			try:
				if await exists(BOT_ID, LOG_CHAT) is False:
					await add_user(
						LOG_CHAT,
						BOT_ID
					)
					print(f"Added bot in log chat . . .\n")
				else:
					print(f"Bot is present in log chat . . .\n")
			except PeerIdInvalid:
				print("Peer id is invalid, Manually send a message in log chat . . .\n")
				pass
			await bot.stop()
		else:
			await get_bot()
			log.warning("Bot is not available, please check (TOKEN, API_ID, API_HASH)")
	except Exception as e:
		print(e)




def uptime():
	""" Bot active time """
	mytime = get_readable_time(time.time() - StartTime)
	return mytime




class tron(Client):
	""" Userbot """
	def __init__(self):
		super().__init__(
		session_name=SESSION,
		api_id=API_ID,
		api_hash=API_HASH,
		app_version=version,
		workers=WORKERS,
		)
	async def sleep(duration=0):
		asyncio.sleep(duration)




class lara(Client):
	""" Assistant """
	def __init__(self):
		super().__init__(
		session_name="lara",
		api_id=API_ID,
		api_hash=API_HASH,
		bot_token=TOKEN,
		)




if SESSION:
	""" Decorator assignment """
	app = tron()
elif not SESSION:
	app = False
	log.warning("Failed to create (app) client, please recheck your credentials.")



if TOKEN:
	""" Decorator assignment """
	bot = lara()
elif not TOKEN:
	bot = False
	log.warning("Failed to create (bot) client, please recheck your credentials.")



