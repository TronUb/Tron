from pyrogram import Client
from .utils import Utils




class SuperClient(Utils, Client):
	""" Userbot (tron) """
	def __init__(self):
		super().__init__(
		session_name=self.SESSION,
		api_id=self.API_ID,
		api_hash=self.API_HASH,
		workers=self.WORKERS,
		)
		self.start()
		self.me = self.get_chat("me")
		self.id = self.me.id
		self.dc_id = self.me.dc_id
		self.name = self.me.first_name
		self.username = f"@{self.me.username}" if self.me.username else ""
		self.bio = self.me.bio if self.me.bio else ""
		self.pic = self.download_media(self.me.photo.big_file_id) if self.me.photo else ""
		self.stop()

		self.bot = self.Bot() # workaround

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
			self.me = self.get_chat("me")
			self.id = self.me.id
			self.dc_id = self.me.dc_id
			self.name = self.me.first_name
			self.username = f"@{self.me.username}"
			self.bio = self.me.bio if self.me.bio else ""
			self.pic = self.download_media(self.me.photo.big_file_id) if self.me.photo else ""
			self.stop()
