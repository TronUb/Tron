import time
import pyrogram
import platform

from logging import getLogger, WARNING, CRITICAL
from pysimplelog import Logger
from config import Config
from telegraph import Telegraph
from tronx.methods import Methods
from pyrogram import __version__ as pyro_version
from pyrogram.types import Message
from tronx.database import Database
from tronx.helpers import Helpers




class Utils(Methods, Config, Database, Helpers):
	# versions /

	userbot_version = "v.0.0.5"
	assistant_version = "v.0.0.1"
	python_version = str(platform.python_version())
	pyrogram_version = str(pyro_version)

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

	getLogger("pyrogram.syncer").setLevel(CRITICAL) # turn off pyrogram logging
	log = Logger(timezone=Config.TIME_ZONE)
	log.set_name("") # Ex: Logger <INFO> some message, `Logger` name will empty 

	# telegraph /

	telegraph = Telegraph()
	telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")

