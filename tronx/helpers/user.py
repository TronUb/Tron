class User(object):
	# instant change of names through database vars
	def UserName(self):
		var = self.getdv("USER_NAME")
		one = var if bool(var) is True else self.USER_NAME
		two = one if one else self.name
		return two if two else None


	# username of bot owner
	def UserUsername(self):
		var = self.getdv("USER_USERNAME")
		one = var if bool(var) is True else self.USER_USERNAME
		two = one if one else self.username
		return two if two else None


	# mention of bot owner
	def UserMention(self):
		return self.MentionMarkdown(self.UserId(), self.UserName()) if self.UserName() and self.UserId() else None


	# telegram id of bot owner
	def UserId(self):
		var = self.getdv("USER_ID")
		one = var if bool(var) is True else self.USER_ID
		two = one if one else self.id
		return two if two else None


	# dc id of bot owner
	def UserDc(self):
		data = self.USER_DC if self.USER_DC else self.dc_id
		return data if data else None


	# custom user pic
	def UserPic(self):
		var = self.getdv("USER_PIC")
		one = var if bool(var) is True else self.USER_PIC
		return one if one else None


	def UserBio(self):
		var = self.getdv("USER_BIO")
		one = var if bool(var) is True else self.USER_BIO
		return one if one else None
