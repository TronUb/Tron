from tronx import app

from tronx.helpers.utils import mention_markdown

from tronx.database.postgres import dv_sql as dv




class User(object):
	# instant change of names through database vars
	def UserName():
		var = dv.getdv("USER_NAME")
		one = var if bool(var) is True else app.USER_NAME
		two = one if one else app.REAL_USER_NAME
		return two if two else None


	# username of bot owner
	def UserUsername():
		var = dv.getdv("USER_USERNAME")
		one = var if bool(var) is True else app.USER_USERNAME
		two = one if one else app.REAL_USER_USERNAME
		return two if two else None


	# mention of bot owner
	def UserMention():
		return mention_markdown(UserId(), UserName()) if UserName() and UserId() else None


	# telegram id of bot owner
	def UserId():
		var = dv.getdv("USER_ID")
		one = var if bool(var) is True else app.USER_ID
		two = one if one else app.REAL_USER_ID
		return two if two else None


	# dc id of bot owner
	def UserDc():
		data = app.USER_DC if app.USER_DC else app.REAL_USER_DC
		return data if data else None
