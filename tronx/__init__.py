import os
import platform


ostype = platform.uname()
is_localhost = True if ostype == "localhost" else False   

if in ("Windows", "Linux") and is_localhost:
	os.system("python -m termux")
	from config import Config

from tronx.clients import app
from tronx.helpers import gen, regex
