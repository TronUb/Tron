import os
import sys
import platform


# for termux deployment // check if its android device
if hasattr(sys, "getandroidapilevel"):
	ostype = "android"
	os.system("cd ostype && python3 -m termux")
	from config import Config

elif platform.uname()[0] == "Linux":
	ostype = "linux"

elif platform.uname()[0] == "Windows":
	ostype = "windows"
else:

	ostype = "unknown"


from tronx.clients import app
from tronx.helpers import gen, regex
