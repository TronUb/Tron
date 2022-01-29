import os
import time
import pyrogram
import platform

from pysimplelog import Logger
from config import Config
from typing import Union, List
from telegraph import Telegraph
from tronx.methods import Methods
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid
from tronx.database import Database
from tronx.helpers import Helpers




class Utils(Methods, Config, Database, Helpers):
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

