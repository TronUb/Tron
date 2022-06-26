import os
import platform



if platform.uname()[0] in ("Windows", "Linux"):
	os.system("python -m termux")
	from config import Config

from tronx.clients import app
from tronx.helpers import gen, regex
