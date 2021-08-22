from config import Config

from tronx.helpers.utils import mention_markdown 

from tronx import get_bot, bot




if bot:
	data = await get_bot()
	BOT_ID = data[0]
	BOT_DC = data[1]
	BOT_NAME = data[2]
	BOT_USERNAME = data[3]
else:
	BOT_ID = None
	BOT_DC = None
	BOT_NAME = None
	BOT_USERNAME = None


def botname():
	if Config.BOT_NAME:
		botname = Config.BOT_NAME
	elif BOT_NAME:
		botname = BOT_NAME
	else:
		botname = None
	return botname


def botusername():
	if Config.BOT_USERNAME:
		botuname = Config.BOT_USERNAME
	elif BOT_USERNAME:
		botuname = BOT_USERNAME
	else:
		botuname = None
	return botuname


def botmention():
	bname = botname()
	bid = botid()
	if bname and bid:
		bmention = mention_markdown(bid, bname)
	else:
		bmention = None
	return bmention


def botid():
	if Config.BOT_ID:
		bid = Config.BOT_ID
	elif BOT_ID:
		bid = BOT_ID
	else:
		bid = None
	return bid