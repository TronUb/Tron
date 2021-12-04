from config import Config

from tronx.helpers.utils import mention_markdown 

try: 
	from tronx import (
		BOT_ID,
		BOT_NAME,
		BOT_USERNAME
		)
except ImportError:
	BOT_ID = Config.BOT_ID if Config.BOT_ID else None
	BOT_NAME = Config.BOT_NAME if Config.BOT_NAME else None
	BOT_USERNAME = Config.BOT_USERNAME if Config.BOT_USERNAME else None     

from tronx.database.postgres import dv_sql as dv




# name of bot (1st priority to database variable)
def botname():
	var = dv.getdv("BOT_NAME")
	var_data = var if bool(var) is True else Config.BOT_NAME
	data = var_data if var_data else BOT_NAME
	return data if data else None


# username of bot
def botusername():
	var = dv.getdv("BOT_USERNAME")
	var_data = var if bool(var) is True else Config.BOT_USERNAME
	data = var_data if var_data else BOT_USERNAME
	return data if data else None


# mention of bot
def botmention():
	return mention_markdown(botid(), botname()) if botid() and bname() else None  


# id of bot 
def botid():
	var = dv.getdv("BOT_ID")
	var_data = var if bool(var) is True else Config.BOT_ID
	data = var_data if var_data else BOT_ID
	return data if data else None



# bio of bot
def bot_bio(m: Message):
	if bool(dv.getdv("BOT_BIO")):
		msg = dv.getdv("BOT_BIO") + "\n\nCatagory: "
	elif Config.BOT_BIO:
		msg = Config.BOT_BIO + "\n\nCatagory: "
	else:
		msg = f"Hey {m.from_user.mention} my name is LARA and I am your assistant bot. I can help you in many ways . Just use the buttons below to get list of possible commands...And Other Functions.\n\nCatagory: "
	return msg




# pic of bot
def bot_pic():
	if bool(dv.getdv("BOT_PIC")):
		_pic = dv.getdv("BOT_PIC")
	elif Config.BOT_PIC:
		_pic = Config.BOT_PIC
	else:
		_pic = False
	return _pic

#End


