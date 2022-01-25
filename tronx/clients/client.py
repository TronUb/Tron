from pyrogram import Client
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
		self.bot = self.Bot()
		self.me = self.get_me()
		self.id = self.me.id
		self.dc_id = self.me.dc_id
		self.name = self.me.first_name
		self.username = "@" + self.me.username if self.me.username else ""
		self.stop()

	class Bot(Client, Utils):
		""" Assistant (Nora) """
		def __init__(self):
			super().__init__(
			session_name="Nora",
			api_id=self.API_ID,
			api_hash=self.API_HASH,
			bot_token=self.TOKEN,
			)
			self.start()
			self.me = self.get_me()
			self.id = self.me.id
			self.dc_id = self.me.dc_id
			self.name = self.me.first_name
			self.username = "@" + self.me.username
			self.stop()
