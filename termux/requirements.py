import os
import re
import pkg_resources
import platform



osname = platform.uname()[0]
dependencies = "Pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir Pillow bs4 covid pySmartDL pyDownload SQLAlchemy==1.3.23 TgCrypto httpx pytz py-postgresql psycopg2 CurrencyConverter deep-translator gTTS git-python Wikipedia-API speedtest-cli==2.1.3 qrcode bing-image-downloader pysimplelog" 



def install_requirements():
	if osname =="Windows":
		os.system("scoop update")
	else:
		os.system("apt update && apt upgrade")
		os.system("pkg update")

	os.system("pip install wheel")
	for x in dependencies.split():
		installed_packages = [p.project_name for p in pkg_resources.working_set]
		pkg = x.split("=")[0]
		if pkg == "Pillow":
			if not pkg in installed_packages:
				print(f"\nInstalling package {x}\n")
				if osname == "Linux": # termux pillow installation failure solution
					print("\nInstalling package {x}\n")
					os.system("pkg install libjpeg-turbo")
					os.system("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/' pip install Pillow")
					os.system("clear")
					continue

		if not pkg in installed_packages:
			print(f"\nInstalling package {x}\n")
			os.system(f"pip3 install {x}")
			os.system("clear")
			

	os.system("clear")



