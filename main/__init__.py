""" everything starts here """

import os

try:
    import pytgcalls
except ImportError:
    os.system("pip3 install pytgcalls")


from config import Config
from main.userbot.client import app
bot = app.bot
from main.core.filters import gen, regex
