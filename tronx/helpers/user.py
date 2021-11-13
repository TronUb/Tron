from tronx import (
	USER_NAME,
	USER_USERNAME,
	USER_ID,
	USER_DC,
	Config,
	)

from tronx.helpers.utils import mention_markdown

from tronx.database.postgres import dv_sql as dv




# instant change of names through database vars
def myname():
	var = dv.getdv("USER_NAME")
	one = var if bool(var) is True else Config.USER_NAME
	two = one if one else USER_NAME
	return two if two else None


# username of bot owner
def myusername():
	var = dv.getdv("USER_USERNAME")
	one = var if bool(var) is True else Config.USER_USERNAME
	two = one if one else USER_USERNAME
	return two if two else None


# mention of bot owner
def mymention():
	return mention_markdown(myid(), myname()) if myname() and myid() else None


# telegram id of bot owner
def myid():
	var = dv.getdv("USER_ID")
	one = var if bool(var) is True else Config.USER_ID
	two = one if one else USER_ID
	return two if two else None


# dc id of bot owner
def mydc():
	data = Config.USER_DC if Config.USER_DC else USER_DC
	return data if data else None
