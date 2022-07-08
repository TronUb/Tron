
OTHERDV = [
	"NO_LOAD",
	"SUDO_USERS",
	"SUDO_CMDS",
	"PREFIX",
	"HELP_EMOJI",
	]



class OtherConfig(object):
	def NoLoad(self):
		""" Get your No load module list """
		noloadvar = self.getdv("NO_LOAD")
		data_list = noloadvar.split() if noloadvar else False  
		return data_list or self.NO_LOAD or [] 


	def SudoUsers(self):
		""" Get sudo users """
		sudovar = self.getdv("SUDO_USERS")
		data_list = [int(x) for x in sudovar.split()] if sudovar else False  
		return data_list or self.SUDO_USERS or [] 



	def Trigger(self):
		""" Get list of prefixes (command handlers) """
		return self.getdv("TRIGGER").split() or self.TRIGGER.split() or "."


	def HelpEmoji(self):
		""" This will return the emoji which will be used in helpdex """
		return self.getdv("HELP_EMOJI") or self.HELP_EMOJI or ""


	def SudoCmds(self):
		""" returns a list of command names """
		return self.getdv("SUDO_CMDS").split() or []




