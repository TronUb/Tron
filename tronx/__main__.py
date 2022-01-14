import os
import importlib
import asyncio

from pyrogram import idle
from tronx.client import (
	app, 
	bot,
	log,
)




loop = asyncio.get_event_loop()


def import_module(path, exclude=[], display_module=True):
	"""Modified version of pyrogram smart plugins"""
	bin = []
	bin.clear()

	if not os.path.exists(path):
		return print(f"No path found: {path}")

	plugins = []
	for x in os.listdir(path):
		if x.endswith(".py"):
			if not x in ["__pycache__",  "__init__.py"]:
				plugins.append(x.replace(".py", ""))

	py_path_raw = ".".join(path.split("/"))
	py_path = py_path_raw[0:len(py_path_raw)-1]

	count = 0
	for x in plugins:
		if not x in exclude:
			importlib.import_module(py_path + "." + x)
			count += 1
			bin.append(x)

	if display_module:
		data = sorted(bin)
		for x in data:
			print(x + " Loaded !")
	return count




async def start_assistant():
	""" Start assistant """
	if bot:
		await bot.start()
		log.info("Assistant activated, startup in progress . . .\n")
	else:
		log.info("Assistant start unsuccessful, please check that you have given the bot token.\n")
		log.info("skipping assistant start !")




async def start_userbot():
	""" Start userbot """
	if app:
		await app.start()
		log.info("Userbot activated, startup in progress . . .\n")
	else:
		log.info("Userbot startup unsuccessful, please check everything again ...")
		log.info("Couldn't load modules of userbot")




async def start_bot():
	""" Main startup """
	print("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	print("initialising . . .\n\n")
	print("Loading plugins:\n\n")
	_plugs = import_module("tronx/plugins/")
	print(f"\n\n{_plugs} modules Loaded\n\n")
	print("Loading modules:\n\n")
	_mods = import_module("tronx/modules/")
	print(f"\n\n{_mods} modules Loaded")
	await start_assistant()
	await start_userbot()
	await idle()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
