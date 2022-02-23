class Others(object):
	def NoLoad(self):
		noloadvar = self.getdv("NO_LOAD")
		data_list = noloadvar.split() if noloadvar else False  
		return data_list or self.NO_LOAD or [] 


	def SudoUsers(self):
		sudovar = self.getdv("SUDO_USERS")
		data_list = [int(x) for x in sudovar.split()] if sudovar else False  
		return data_list or self.SUDO_USERS or [] 


	def Pmpermit(self):
		return self.getdv("PMPERMIT") or self.PMPERMIT or None


	def PmpermitLimit(self):
		return self.getdv("PM_LIMIT") or self.PM_LIMIT or 4


	def PmpermitPic(self):
		return self.getdv("PMPERMIT_PIC") or self.PMPERMIT_PIC or None


	def PmpermitText(self):
		return self.getdv("PMPERMIT_TEXT") or self.PMPERMIT_TEXT or None


	def MyPrefix(self):
		return self.getdv("PREFIX").split() or self.PREFIX.split() or "."


	def HelpEmoji(self):
		return self.getdv("HELP_EMOJI") or self.HELP_EMOJI or ""
		


