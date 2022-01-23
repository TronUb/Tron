import os
from pyrogram import Client
from .tempclient import utils



if not os.path.exists("downloads"):
	""" all files are downloaded here """
	os.mkdir("downloads")



class Tron(Client, utils):
	""" Userbot """
	from tronx.helpers import Helpers

	def __init__(self):
		super().__init__(
		session_name=self.SESSION,
		api_id=self.API_ID,
		api_hash=self.API_HASH,
		workers=self.WORKERS,
		)
       
	class bot(Client, utils):
		""" Assistant """
		def __init__(self):
			super().__init__(
			session_name="Nora",
			api_id=self.API_ID,
			api_hash=self.API_HASH,
			bot_token=self.TOKEN,
			)





app = Tron() 
bot = Tron.bot()







