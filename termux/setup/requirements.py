import os
import subprocess
from time import sleep
import pkg_resources



dependencies = "Pyrogram==2.0.27 pytube telegraph heroku3 aiohttp aiofiles hachoir Pillow bs4 covid pySmartDL pyDownload SQLAlchemy==1.3.23 TgCrypto httpx pytz py-postgresql psycopg2 CurrencyConverter deep-translator gTTS git-python Wikipedia-API speedtest-cli==2.1.3 qrcode bing-image-downloader pysimplelog" 


# run shell commands
def shell(args: str):
	return subprocess.run(args.split(), capture_output=True).stdout.decode("ascii")


# clear screen
def clear():
	return shell("clear")


# upgrade linux packages
def update_upgrade(msg: str, clear_screen: bool=True):
	clear()
	print(msg + "\n\n")
	output = shell("apt update") + "\n\n"
	output += shell("apt upgrade")
	if clear_screen:
		clear()
	return output


# check & install python if not installed
def check_python(msg: str):
	print(msg + "\n\n")
	output = shell("python3 -V")
	if "No command python3 found" in output:
		print("\n\nPython is not installed: installing . . .\n\n")
		shell("apt install python3")
		clear()
	else:
		print("Python is already installed.")
		sleep(1)
		clear()


# install wheel 
def install_wheel():
	return shell("pip3 install wheel")
	clear()
	


# install requirements 
def install_requirements():
	update_upgrade("Updating and upgrading ...")
	check_python("Checking python . . .")
	install_wheel()

	for x in dependencies.split():
		installed_packages = [p.project_name for p in pkg_resources.working_set]
		pkg = x.split("=")[0]

		if not pkg in installed_packages:
			if pkg == "Pillow":
				print(f"\nInstalling package {x}\n\n")
				shell("pkg install libjpeg-turbo")
				shell("LDFLAGS='-L/system/lib64/' CFLAGS='-I/data/data/com.termux/files/usr/include/') 
				shell("pip3 install Pillow")
				clear()
				continue

			print(f"\nInstalling package {x}\n\n")
			shell(f"pip3 install {x}")
			clear()
	clear()
	return True



