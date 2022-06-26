import os
import platform


ostype = platform.uname()
is_localhost = True if ostype[1] == "localhost" else False   

if ostype[0] in ("Windows", "Linux") and is_localhost:
	os.system("python -m termux")
	from config import Config

from tronx.clients import app
from tronx.helpers import gen, regex
