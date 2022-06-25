import os
import re
import pkg_resources




dependencies = "pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir bs4 covid pySmartDL pyDownload sqlalchemy==1.3.23 tgcrypto httpx pytz py-postgresql psycopg2 currencyconverter deep_translator gtts git-python wikipedia-api speedtest-cli==2.1.3"


def install_requirements():
	os.system("apt update")
	os.system("pkg update")
	os.system("pkg install python3")
	os.system("pip install wheel")
	for x in dependencies.split():
		installed_packages = [p.project_name for p in pkg_resources.working_set]
		pkg = x.split("=")[0]
		if pkg == "pillow":
			if not pkg in installed_packages:
				print(f"\nInstalling package {x}\n")
				os.system("pkg install libjpeg-turbo")
				os.system("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/' pip install Pillow")
				os.system("clear")
				continue

		if not pkg in installed_packages:
			print(f"\nInstalling package {x}\n")
			os.system(f"pip3 install {x}")
			os.system("clear")
			

	os.system("clear")



