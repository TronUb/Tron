import os
import sys
import time
import logging

from pyrogram import Client
from pyrogram.filters import Filter
from pyrogram import filters

from telegraph import Telegraph

from config import Config




# debugging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)




# /app/tronx/modules/telegraph.py
telegraph = Telegraph()
telegraph.create_account(short_name='Tron Userbot') 




# variables
PREFIX = Config.PREFIX

LOG_CHAT = Config.LOG_CHAT

OWNER_NAME = "࿇•ẞᗴᗩSԵ•࿇"

OWNER_ID = 1790546938

OWNER_USERNAME = "@BEASTZX"

version = "v.0.0.1"

CMD_HELP = {}

HELP = {}

REPO = "https://github.com/beastzx18/Tron"

StartTime = time.time()




# This bot is only compatiable with python versions >= 3.9.0
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
	log.error(
		"python version 3.9.0 or greater is required, bot quitting !"
		)
	quit(1)




# to log errors, mentions, etc
if not Config.LOG_CHAT:
	log.warning(
		"LOG_CHAT is important for bots normal working, please fill it."
		)
	quit(1)




# time converter 
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




# get some required information of user
async def get_self():
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




# get some required information of bot
async def get_bot():
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




# add users
async def add_user(userid: int, chatid: str):
	try:
		await app.add_chat_members(
			chatid, 
			userids
			)
	except Exception as e:
		print(e)
		pass




async def userlise():
	await app.start()
	await get_self()
	try:
		await app.resolve_peer(
			Config.LOG_CHAT
			)
		await add_user(
			Config.LOG_CHAT,
			BOT_ID
			)
	except Exception as e:
		print(e)
		pass
	await app.stop()




async def botlise():
	if bot:
		await bot.start()
		await get_bot()
		await bot.stop()
	else:
		pass
		await get_bot()




# userbot active time
def uptime():
	mytime = get_readable_time(time.time() - StartTime)
	return mytime




# Userbot
class tron(Client):
	def __init__(self):
		super().__init__(
		session_name=Config.SESSION,
		api_id=Config.API_ID,
		api_hash=Config.API_HASH,
		app_version=version,
		workers=Config.WORKERS,
		)




# Assistant
class lara(Client):
	def __init__(self):
		super().__init__(
		session_name="lara",
		api_id=Config.API_ID,
		api_hash=Config.API_HASH,
		bot_token=Config.TOKEN,
		)




# assigning decorators
if Config.SESSION:
	app = tron()
else:
	app = False
	log.warning("String session is missing, please fill this requirement !")




if Config.TOKEN:
	bot = lara()
else:
	bot = False
	log.warning("Bot token is missing, please fill this requirement !")



