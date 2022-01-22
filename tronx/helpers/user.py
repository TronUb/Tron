from tronx.database.postgres import dv_sql as dv




class User(object):
	# instant change of names through database vars
	def UserName(self):
		var = dv.getdv("USER_NAME")
		one = var if bool(var) is True else self.USER_NAME
		two = one if one else self.REAL_USER_NAME
		return two if two else None


	# username of bot owner
	def UserUsername(self):
		var = dv.getdv("USER_USERNAME")
		one = var if bool(var) is True else self.USER_USERNAME
		two = one if one else self.REAL_USER_USERNAME
		return two if two else None


	# mention of bot owner
	def UserMention(self):
		return self.mention_markdown(self.UserId(), self.UserName()) if self.UserName() and self.UserId() else None


	# telegram id of bot owner
	def UserId(self):
		var = dv.getdv("USER_ID")
		one = var if bool(var) is True else self.USER_ID
		two = one if one else self.REAL_USER_ID
		return two if two else None


	# dc id of bot owner
	def UserDc(self):
		data = self.USER_DC if self.USER_DC else self.REAL_USER_DC
		return data if data else None
