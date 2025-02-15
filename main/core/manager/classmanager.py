import time
import logging
import platform

from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version

from main import Config
from main.core.methods import Methods


# pylint: disable=E1101
class ClassManager(Config, Methods):
    """Manages bot configurations, logging, and telegraph setup."""

    # Versions
    python_version: str = platform.python_version()
    pyrogram_version: str = pyrogram_version

    # Assistant
    assistant_name: str = "Nora"
    assistant_version: str = "v.0.0.5"

    # Userbot
    userbot_name: str = "Tron"
    userbot_version: str = "v.0.2.0"

    # Owner Details
    owner_name: str = "࿇•ẞᗴᗩSԵ•࿇"
    owner_id: int = 1790546938
    owner_username: str = "@BEASTZX"

    # Repository and Resources
    repo_url: str = "https://github.com/TronUb/Tron.git"
    pic_url: str = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"

    # Containers
    CMD_HELP = {}
    message_ids = {}
    whisper_ids = {}
    callback_user = None

    # Start Time
    start_time = time.time()

    # Logging Setup
    @staticmethod
    def setup_logging():
        """Configures logging settings for the bot."""
        logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
        logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.session.internals.msg_id").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.dispatcher").setLevel(logging.WARNING)
        logging.getLogger("pyrogram.connection.connection").setLevel(logging.WARNING)

    log = logging.getLogger()
    setup_logging()

    # Telegraph Setup
    try:
        telegraph = Telegraph()
        telegraph.create_account(short_name=Config.TL_NAME or "TronUserbot Team")
        log.info("Telegraph account created successfully.")
    except Exception as e:
        log.error("Failed to initialize Telegraph: %s", e)
        telegraph = None
