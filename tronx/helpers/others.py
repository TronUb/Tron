class Others(object):
	def NoLoad(self):
		noloadvar = self.getdv("NO_LOAD")
		data_list = [int(x) for x in noloadvar.split()] if noloadvar else False  
		return data_list or self.NO_LOAD or [] 


	def SudoUsers(self):
		sudovar = self.getdv("SUDO_USERS")
		data_list = [int(x) for x in sudovar.split()] if sudovar else False  
		return data_list or self.SUDO_USERS or [] 

