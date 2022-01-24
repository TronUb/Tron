from pyrogram import Client, idle
from .utils import Utils




class SuperClient(Client, Utils):
	""" Userbot (tron) """
	def __init__(self):
		super().__init__(
		session_name=self.SESSION,
		api_id=self.API_ID,
		api_hash=self.API_HASH,
		workers=self.WORKERS,
		)
		self.start()
		idle()

	def tron(self):
		return self.get_me()

	def dc_id(self):
		return (self.get_me())

	def id(self):
		return (self.get_me())

	def name(self):
		return (self.get_me())

	def username(self):
		return "@" + (self.get_me()) if (self.get_me()) else ""


	class bot(Client, Utils):
		""" Assistant (Nora) """
		def __init__(self):
			super().__init__(
			session_name="Nora",
			api_id=self.API_ID,
			api_hash=self.API_HASH,
			bot_token=self.TOKEN,
			)
			self.start()
			idle()

		def nora(self):
			return self.bot.get_me()

		def dc_id(self):
			return (self.bot.get_me())

		def id(self):
			return (self.bot.get_me())

		def name(self):
			return (self.bot.get_me())

		def username(self):
			return "@" + (self.bot.get_me())

