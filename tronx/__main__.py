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
	if not os.path.exists(path):
		return print(f"No path found: {path}")

	plugins = []
	for x in os.listdir(path):
		if x.endswith(".py"):
			if not x in ["__pycache__",  "__init__.py"]:
				plugins.append(x.replace(".py", ""))

	py_path_raw = ".".join(path.split("/"))
	py_path = py_path_raw[0:len(py_path_raw)-1]

	for x in plugins:
		if not x in exclude:
			importlib.import_module(py_path + "." + x)
			if display_module:
				print(x + " Loaded !")



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
	log.info("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	log.info("initialising . . .\n\n")
	log.info("Loading modules:\n\n")
	import_module("tronx/modules/")
	log.info("Loading plugins:\n\n")
	import_module("tronx/plugins/")
	await start_assistant()
	await start_userbot()
	await idle()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
