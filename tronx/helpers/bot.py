from config import Config

from tronx.helpers.utils import mention_markdown 

try: 
	from tronx import (
		BOT_ID,
		BOT_NAME,
		BOT_USERNAME
		)
except ImportError:
	BOT_ID = None
	BOT_NAME = None
	BOT_USERNAME = Config.BOT_USERNAME




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

