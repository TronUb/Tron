import os
import re
import importlib.util




dependencies = "pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir bs4 covid pySmartDL pyDownload sqlalchemy==1.3.23 tgcrypto httpx pytz py-postgresql psycopg2 currencyconverter deep_translator gtts git-python wikipedia-api speedtest-cli==2.1.3"


def install_requirements():
	os.system("apt update")
	os.system("pkg update")
	os.system("pkg install python3")
	os.system("pip install wheel")
	for pkg in dependencies.split():
		spec = importlib.util.find_spec(pkg.split("=")[0])
		if pkg == "pillow":
			os.system("pkg install libjpeg-turbo")
			os.system("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/' pip install Pillow")
			os.system("clear")
			continue

		if spec is None:
			print(f"\nInstalling package {pkg}\n")
			os.system(f"pip3 install {pkg}")
			os.system("clear")
			

	os.system("clear")



