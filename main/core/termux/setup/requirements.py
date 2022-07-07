import os
from time import sleep
import pkg_resources



dependencies = "Pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir Pillow bs4 covid pySmartDL pyDownload SQLAlchemy==1.3.23 TgCrypto httpx pytz py-postgresql psycopg2 CurrencyConverter deep-translator gTTS git-python Wikipedia-API speedtest-cli==2.1.3 qrcode bing-image-downloader pysimplelog" 


def clear():
	os.system("clear")


def install_requirements():
	clear()
	print("updating and upgrading ...\n\n")
	sleep(0.5)
	os.system("apt update && apt upgrade")
	clear()

	print("Installing python3 ...\n\n")
	sleep(0.5)
	os.system("apt install python3")
	os.system("pip3 install wheel")
	clear()

	for x in dependencies.split():
		installed_packages = [p.project_name for p in pkg_resources.working_set]
		pkg = x.split("=")[0]

		if not pkg in installed_packages:
			if pkg == "Pillow":
				print(f"\nInstalling package {x}\n\n")
				os.system("pkg install libjpeg-turbo")
				os.system("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/' pip3 install Pillow")
				clear()
				continue

			print(f"\nInstalling package {x}\n\n")
			os.system(f"pip3 install {x}")
			clear()
	clear()
	return True



