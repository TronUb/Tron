""" this file determines deployment method """

import os
import sys


# for termux deployments
# check if the current device is android
if hasattr(sys, "getandroidapilevel"):
    os.system("python3 -m termux")
    from config import Config


from main.userbot.client import app # pylint: disable=wrong-import-position
bot = app.bot
from main.core.filters import gen, regex # pylint: disable=wrong-import-position
