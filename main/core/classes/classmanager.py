import time
import logging 
import platform

from config import Config
from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version
from main.core.database import Database
from main.core.helpers import Helpers
from main.core.newpyrogram import Methods






class ClassManager(Config, Helpers, Database, Methods):
    # versions /
    python_version = str(platform.python_version())
    pyrogram_version = str(pyrogram_version)

    # assistant /
    assistant_name = "Nora"
    assistant_version = "v.0.0.2"

    # userbot /
    userbot_name = "Tron"
    userbot_version = "v.0.1.3"

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
    utube_object = object

    # debugging /
    
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

    # telegraph /
    telegraph = Telegraph()
    telegraph.create_account(short_name=Config.TL_NAME if Config.TL_NAME else "Tron userbot")

