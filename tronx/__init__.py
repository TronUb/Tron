import os
import sys


# for termux deployments 
# check if the current device is android
if hasattr(sys, "getandroidapilevel"):
	os.system("python3 -m termux")
	from config import Config


from tronx.clients import app
from tronx.helpers import gen, regex
