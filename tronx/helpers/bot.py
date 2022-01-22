from tronx.database.postgres import dv_sql as dv
from pyrogram.types import Message




class Bot(object):
	def BotName(self):
		"""Get your bot name"""
		var = dv.getdv("BOT_NAME")
		var_data = var if bool(var) is True else self.BOT_NAME
		data = var_data if var_data else self.REAL_BOT_NAME
		return data if data else None

	def BotUserName(self):
		"""Get your bot username"""
		var = dv.getdv("BOT_USERNAME")
		var_data = var if bool(var) is True else self.BOT_USERNAME
		data = var_data if var_data else self.REAL_BOT_USERNAME
		return data if data else None

	def BotMention(self):
		"""Get bot mention"""
		return f"[{self.BotName()}](tg://user?id={self.BotId()})" if BotId() and BotName() else None  


	def BotId(self):
		"""Get your bots telegram id"""
		var = dv.getdv("BOT_ID")
		var_data = var if bool(var) is True else self.BOT_ID
		data = var_data if var_data else self.REAL_BOT_ID
		return data if data else None


	def BotBio(self, m: Message):
		"""Get your bots bio"""
		msg = f"Hey {m.from_user.mention} my name is {self.assistant_name} and I am your assistant bot. I can help you in many ways . Just use the buttons below to get list of possible commands."  
		var = dv.getdv("BOT_BIO")
		var_data = var if bool(var) else self.BOT_BIO
		data = var_data if var_data else msg
		return f"{data}\n\nCatagory: " if data else None


	def BotPic(self):
		"""Get your bot pic url"""
		var = dv.getdv("BOT_PIC")
		var_data = var if bool(var) else self.BOT_PIC
		data = var_data if bool(var_data) else False
		return data if data else None
	
