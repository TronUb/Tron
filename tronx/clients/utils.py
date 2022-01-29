import os
import time
import logging
import pyrogram
import platform
import importlib
import subprocess

from pysimplelog import Logger
from config import Config
from typing import Union, List
from telegraph import Telegraph
from tronx.methods import Methods
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid
from tronx.database import Database
from tronx.helpers import Helpers




class Collector(Methods, Config, Database, Helpers):
	# versions /

	userbot_version = "v.0.0.5"
	assistant_version = "v.0.0.1"
	python_version = str(platform.python_version())
	pyrogram_version = str(pyrogram.__version__)

	# containers /

	CMD_HELP = {}

	# owner details /

	owner_name = "࿇•ẞᗴᗩSԵ•࿇"
	owner_id = 1790546938
	owner_username = "@BEASTZX"

	# other /

	Repo = "https://github.com/beastzx18/Tron"
	StartTime = time.time()

	# debugging /

	log = Logger(__name__)

	# telegraph /

	telegraph = Telegraph()
	telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")





class Utils(Collector):
	def clear():
		""" clear terminal logs """
		subprocess.call("clear" if os.name == "posix" else "cls") 


	def add_user(self, user_id: Union[int, List[int]], chat_id: str):
		""" Add users in groups / channels """
		try:
			done = self.add_chat_members(chat_id, user_id)
			return True if done else False
		except Exception as e:
			print(e)


	def exists(self, user_id: int, chat_id: str):
		for x in self.iter_chat_members(chat_id):
			if x.user.id == user_id:
				return True
		

	def check_bot_in_log_chat(self):
		try:
			if bot:
				print("Checking presence of bot in log chat . . .\n")
				try:
					if self.exists(self.bot.id, self.LOG_CHAT) is False:
						self.add_user(self.LOG_CHAT, self.bot.id)
						print(f"Added bot in log chat . . .\n")
					else:
						print(f"Bot is already present in log chat . . .\n")
				except PeerIdInvalid:
					print("Peer id is invalid, Manually send a message in log chat . . .\n")

			else:
				self.log.warning("Bot is not available, please check (TOKEN, API_ID, API_HASH)")
		except Exception as e:
			print(e)


	def uptime(self):
		""" Bot active time """
		return self.GetReadableTime(time.time() - self.StartTime)


	def import_module(self, path, exclude=[], display_module=True):
		"""Modified version of pyrogram smart plugins"""
		bin = []
		bin.clear()

		if not os.path.exists(path):
			return print(f"No path found: {path}")

		plugins = []
		for x in os.listdir(path):
			if x.endswith(".py"):
				if not x in ["__pycache__",  "__init__.py"]:
					plugins.append(x.replace(".py", ""))

		py_path_raw = ".".join(path.split("/"))
		py_path = py_path_raw[0:len(py_path_raw)-1]

		count = 0
		for x in plugins:
			if not x in exclude:
				importlib.import_module(py_path + "." + x)
				count += 1
				bin.append(x)

		if display_module:
			data = sorted(bin)
			for x in data:
				print(x + " Loaded !")
		return count


	def db_status(self):
		"Available" if self.DB_URI else "Unavailable"


