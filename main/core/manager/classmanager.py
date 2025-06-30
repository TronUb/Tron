import time
import logging
import platform

from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version

from main import Config
from main.core.methods import Methods

# pylint: disable=no-member

class ClassManager(Config, Methods):
    """Manages bot configurations, logging, and telegraph setup."""

    # Static Versions
    python_version: str = platform.python_version()
    pyrogram_version: str = pyrogram_version

    # Assistant & Userbot Info
    assistant_name: str = "Nora"
    assistant_version: str = "v.0.0.5"
    userbot_name: str = "Tron"
    userbot_version: str = "v.0.2.0"

    # Owner Info (should ideally come from Config/env)
    owner_name: str = Config.USER_NAME or "࿇•ẞᗴᗩSԵ•࿇"
    owner_id: int = int(Config.USER_ID or 1790546938)
    owner_username: str = Config.USER_USERNAME or "@BEASTZX"

    # Project Info
    repo_url: str = "https://github.com/TronUb/Tron.git"
    pic_url: str = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"

    # Runtime Containers
    CMD_HELP = {}
    message_ids = {}
    whisper_ids = {}
    callback_user = None

    # Start Time
    start_time = time.time()

    # Logging Setup
    @staticmethod
    def setup_logging():
        logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
        logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.session.internals.msg_id").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.dispatcher").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.connection.connection").setLevel(logging.WARNING)

    @classmethod
    def initialize(cls):
        cls.setup_logging()
        cls.log = logging.getLogger()

        try:
            cls.telegraph = Telegraph()
            cls.telegraph.create_account(short_name=cls.TL_NAME or "TronUserbot Team")
            cls.log.info("Telegraph account created successfully.")
        except Exception as e:
            cls.log.error("Failed to initialize Telegraph: %s", e)
            cls.telegraph = None
