from tronx import (
	BOT_ID,
	BOT_NAME,
	BOT_USERNAME,
	Config
)

from tronx.database.postgres import dv_sql as dv
from pyrogram.types import Message




def botname():
	"""Get your bot name"""
	var = dv.getdv("BOT_NAME")
	var_data = var if bool(var) is True else Config.BOT_NAME
	data = var_data if var_data else BOT_NAME
	return data if data else None


def botusername():
	"""Get your bot username"""
	var = dv.getdv("BOT_USERNAME")
	var_data = var if bool(var) is True else Config.BOT_USERNAME
	data = var_data if var_data else BOT_USERNAME
	return data if data else None


def botmention():
	"""Get bot mention"""
	return f"[{botname()}](tg://user?id={botid()})" if botid() and botname() else None  


def botid():
	"""Get your bots telegram id"""
	var = dv.getdv("BOT_ID")
	var_data = var if bool(var) is True else Config.BOT_ID
	data = var_data if var_data else BOT_ID
	return data if data else None


def bot_bio(m: Message):
	"""Get your bots bio"""
	msg = f"Hey {m.from_user.mention} my name is LARA and I am your assistant bot. I can help you in many ways . Just use the buttons below to get list of possible commands.\n\nCatagory: "  
	var = dv.getdv("BOT_BIO")
	var_data = f"{var}\n\nCatagory: " if bool(var) else f"{Config.BOT_BIO}\n\nCatagory: "
	data = var_data if var_data else msg
	return data if data else None


def bot_pic():
	"""Get your bot pic url"""
	var = dv.getdv("BOT_PIC")
	var_data = var if bool(var) else Config.BOT_PIC
	data = var_data if bool(var_data) else False
	return data if data else None
	
