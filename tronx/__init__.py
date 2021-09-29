import os
import sys
import time
import logging
import platform

from pyrogram import Client, filters
from pyrogram.filters import Filter
from pyrogram.errors import PeerIdInvalid

from typing import Union, List

from telegraph import Telegraph

from config import Config




# debugging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)




# variables
PREFIX = Config.PREFIX

LOG_CHAT = Config.LOG_CHAT

OWNER_NAME = "࿇•ẞᗴᗩSԵ•࿇"

OWNER_ID = 1790546938

OWNER_USERNAME = "@BEASTZX"

version = "v.0.0.3"

lara_version = "v.0.0.1"

CMD_HELP = {}

HELP = {}

REPO = "https://github.com/beastzx18/Tron"

StartTime = time.time()

__python_version__ = f"{platform.python_version()}"




if Config.DB_URI:
	db_status = "Available"
else:
	db_status = "Not Available"




if sys.version_info[0] < 3 or sys.version_info[1] < 9:
	""" lower version will produce errors in bot """
	log.error(
		"python version 3.9.0 or greater is required, bot is quitting !"
		)
	quit(1)




if not LOG_CHAT:
	""" log chat are required """
	log.warning(
		"LOG_CHAT is important for bots normal working, please fill it."
		)
	quit(1)




def get_readable_time(seconds: int) -> str:
	""" seconds to readable time converter """
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




async def get_self():
	""" Get self information for later use """
	global USER_ID, USER_NAME, USER_USERNAME
	getself = await app.get_me()
	if getself:
		if getself.last_name and getself.username:
			# sometimes users don't have the last name 
			USER_NAME = f"{getself.first_name} {getself.last_name}"
			USER_USERNAME = f"@{getself.username}"
		else:
			# use first name 
			USER_NAME = getself.first_name
			USER_USERNAME = None
		USER_ID = getself.id
		USER_DC = getself.dc_id
	else:
		pass
	return (
		USER_ID, 
		USER_DC,
		USER_NAME, 
		USER_USERNAME
		)




async def get_bot():
	""" Get bot information for later use """
	global BOT_ID, BOT_NAME, BOT_USERNAME
	if bot:
		getbot = await bot.get_me()
		# bot have all permanent infos
		BOT_ID = getbot.id
		BOT_DC = getbot.dc_id
		BOT_NAME = getbot.first_name
		BOT_USERNAME = "@" + getbot.username
	else:
		pass
	return (
		BOT_ID, 
		BOT_DC, 
		BOT_NAME, 
		BOT_USERNAME
		)




async def add_user(user_id: Union[int, List[int]], chat_id: str):
	""" Add users in groups/channels """
	try:
		await app.add_chat_members(
			chat_id, 
			user_id
			)
	except Exception as e:
		print(e)
		pass




# check if the bot is in log chat 
async def exists(user_id: int, chat_id: str):
	_data = []
	_data.clear()
	lime = await app.get_chat_members(chat_id)

	for x in lime:
		_data.append(x.user.id)
	if user_id in _data:
		return True
	else:
		return False




async def userlise():
	global telegraph
	try:
		if app:
			await app.start()
			await get_self()
			telegraph = Telegraph()
			telegraph.create_account(short_name=USER_NAME if USER_NAME else "Tron userbot") 
			await botlise()
			await app.stop()
		else:
			pass
	except Exception as e:
		print(e)




async def botlise():
	if bot:
		await bot.start()
		await get_bot()
		print("Checking presence of bot in log chat . . .")
		try:
			if await exists(BOT_ID, LOG_CHAT) is True:
				await add_user(
					LOG_CHAT,
					BOT_ID
				)
				print(f"Bot is present in log chat . . .")
			else:
				print(f"Bot is not present in log chat, adding bot in log chat . . .")
		except PeerIdInvalid:
			print("Peer id is invalid, Manually send a message in log chat . . .")
			pass
		await bot.stop()
	else:
		await get_bot()




def uptime():
	""" Bot active time """
	mytime = get_readable_time(time.time() - StartTime)
	return mytime




class tron(Client):
	""" Userbot """
	def __init__(self):
		super().__init__(
		session_name=Config.SESSION,
		api_id=Config.API_ID,
		api_hash=Config.API_HASH,
		app_version=version,
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




if Config.SESSION:
	""" Decorator assignment """
	app = tron()
elif not Config.SESSION and list(platform.uname())[1] == "localhost":
	app = Client(config_file="./config.ini")
elif not Config.SESSION and list(platform.uname())[1] != "localhost":
	app = False
	log.warning("String session is missing, please fill this requirement !")




if Config.TOKEN:
	""" Decorator assignment """
	bot = lara()
elif not Config.TOKEN and list(platform.uname())[1] == "localhost":
	bot = Client("lara", config_file="./config.ini")
elif not Config.TOKEN and list(platform.uname())[1] != "localhost":
	bot = False
	log.warning("Bot token is missing, please fill this requirement !")



