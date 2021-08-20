from config import Config

from tronx import (
	USER_NAME,
	USER_USERNAME,
	USER_ID,
	)

from tronx.helpers.utils import mention_markdown





# my name
def myname():
	if Config.USER_NAME:
		name = Config.USER_NAME
	elif USER_NAME:
		name = USER_NAME
	else:
		name = None
	return name


# my username
def myusername():
	if Config.USER_USERNAME:
		username = Config.USER_USERNAME
	elif USER_USERNAME:
		username = USER_USERNAME
	else:
		username = None
	return username


# my mention
def mymention():
	user_name = myname()
	if user_name:
		mention = mention_markdown(USER_ID, user_name)
	else:
		mention = None
	return mention


# my id
def myid():
	if Config.USER_ID:
		userid = Config.USER_ID
	elif USER_ID:
		userid = USER_ID
	else:
		userid = None
	return userid