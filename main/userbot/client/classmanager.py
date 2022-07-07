import time
import logging 
import platform

from config import Config
from telegraph import Telegraph
from main.core import Core
from pyrogram import __version__ as pyrogram_version





class ClassManager(Core, Config):
	# versions /
	python_version = str(platform.python_version())
	pyrogram_version = str(pyrogram_version)

	# assistant /
	assistant_name = "Nora"
	assistant_version = "v.0.0.2"

	# userbot /
	userbot_name = "Tron"
	userbot_version = "v.0.1.2"

	# containers /
	CMD_HELP = {}

	# owner details /
	owner_name = "࿇•ẞᗴᗩSԵ•࿇"
	owner_id = 1790546938
	owner_username = "@BEASTZX"

	# other /
	message_ids = {}
	PIC = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"
	Repo = "https://github.com/TronUb/Tron.git"
	StartTime = time.time()

	# debugging /
	
	logging.basicConfig(filename="tronuserbot.txt", format="%(asctime)s %(message)s", filemode="w")
	log = logging.getLogger()
	log.setLevel(logging.DEBUG)

	# telegraph /
	telegraph = Telegraph()
	telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")

