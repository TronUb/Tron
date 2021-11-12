from config import Config

from tronx import (
	USER_NAME,
	USER_USERNAME,
	USER_ID,
	
	)

from tronx.helpers.utils import mention_markdown

from tronx.database.postgres import dv_sql as dv




# my name
def myname():
	uname = dv.getdv("USER_NAME")
	one = uname if bool(uname) if True else Config.USER_NAME
	two = one if one else USER_NAME
	return two if two else None


# my username
def myusername():
	data = Config.USER_USERNAME if Config.USER_USERNAME else USER_USERNAME
	return data if data else None


# my mention
def mymention():
	return mention_markdown(myid(), myname()) if myname() and myid() else None


# my id
def myid():
	data = Config.USER_ID if Config.USER_ID else USER_ID
	return data if data else None


# my dc
def mydc():
	data = Config.USER_DC if Config.USER_DC else USER_DC
	return data if data else None
