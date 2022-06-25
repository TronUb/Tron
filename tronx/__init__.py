import os



if os.uname()[1] == "localhost":
	os.system("python3 -m termux")
	from config import Config

from tronx.clients import app
from tronx.helpers import gen, regex
