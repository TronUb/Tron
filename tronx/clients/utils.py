import time
import platform

import logging 
from config import Config
from telegraph import Telegraph
from tronx.pyrogramx.methods import Methods
from pyrogram import __version__ as pyrogram_version
from tronx.database import Database
from tronx.helpers import Helpers




class Utils(Methods, Config, Database, Helpers):
	# versions /
	python_version = str(platform.python_version())
	pyrogram_version = str(pyrogram_version)

	# assistant /
	assistant_name = "Nora"
	assistant_version = "v.0.0.1"
	assistant_age = "19"
	assistant_gender = "Female"

	# userbot /
	userbot_name = "Tron"
	userbot_version = "v.0.1.0"

	# containers /
	CMD_HELP = {}

	# owner details /
	owner_name = "࿇•ẞᗴᗩSԵ•࿇"
	owner_id = 1790546938
	owner_username = "@BEASTZX"

	# other /
	message_ids = {}
	PIC = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"
	Repo = "https://github.com/beastzx18/Tron.git"
	StartTime = time.time()

	# debugging /
	logging.getLogger("pyrogram.syncer").setLevel(logging.CRITICAL) # turn off pyrogram logging
	logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
	
	logging.basicConfig(filename="tronuserbot.log", format="%(asctime)s %(message)s", filemode="w")
	log = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	# telegraph /
	telegraph = Telegraph()
	telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")

