"manages all necessary classes"

import time
import logging
import platform
import os

from telegraph import Telegraph
from pyrogram import __version__ as pyrogram_version

from main import Config
from main.core.methods import Methods


# pylint: disable=W1508, W0718
class ClassManager(Config, Methods):
    """Manages bot configurations, logging, and Telegraph setup."""

    # Versions
    python_version: str = platform.python_version()
    pyrogram_version: str = pyrogram_version

    # Assistant
    assistant_name: str = "Nora"
    assistant_version: str = "v.0.0.5"

    # Userbot
    userbot_name: str = "Tron"
    userbot_version: str = "v.0.2.0"

    # Owner Details (Using env variables for security)
    owner_name: str = "࿇•ẞᗴᗩSԵ•࿇"
    owner_id: int = int(os.getenv("OWNER_ID", 1790546938))  # Default: @BEASTZX
    owner_username: str = os.getenv("OWNER_USERNAME", "@BEASTZX")

    # Repository and Resources
    repo_url: str = "https://github.com/TronUb/Tron.git"
    pic_url: str = (
        "https://telegra.ph/file/38eec8a079706b8c19eae.jpg"  # Fixed image URL
    )

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

    setup_logging()  # Ensure logging is set up before getting the logger
    log = logging.getLogger()

    # Telegraph Setup
    @classmethod
    def setup_telegraph(cls):
        """Initializes Telegraph account with proper error handling."""
        try:
            cls.telegraph = Telegraph()
            cls.telegraph.create_account(
                short_name=getattr(Config, "TL_NAME", "TronUserbot Team")
            )
            cls.log.info("Telegraph account created successfully.")
        except Exception as e:
            cls.log.error("Failed to initialize Telegraph: %s", e)
            cls.telegraph = None


# Initialize Telegraph
ClassManager.setup_telegraph()
