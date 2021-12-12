import os
import time
import importlib
import asyncio
import subprocess

from pyrogram import idle

from tronx import (
	app, 
	bot, 
	log, 
)




loop = asyncio.get_event_loop()




def load_plugins():
	""" Assistant modules """
	from tronx.plugins import PLUGINS
	log.info("Loading plugins of [ assistant ], Please wait...\n")
	for plug in PLUGINS:
		importlib.import_module("tronx.plugins." + plug)

	log.info("-----------------------")
	log.info("List of Plugins:\n\n")
	for x in PLUGINS:
		print(x + " Loaded !")
	num_plug = len(PLUGINS)
	log.info(f"\nTotal {num_plug} Plugins Loaded !")
	log.info("-----------------------\n\n")




async def load_modules():
	""" Userbot modules """
	from tronx.modules import MODULES

	log.info("Loading modules of [ Userbot ], Please wait ...\n")
	for plug in MODULES:
		importlib.import_module("tronx.modules." + plug)

	log.info("-----------------------")
	log.info("List Of Modules:\n\n")
	for y in MODULES:
		print(y + " Loaded !")
	num_mod = len(MODULES)
	log.info(f"\nTotal {num_mod} Modules Loaded !")
	log.info("-----------------------\n\n")
	log.info("Try .ping or .alive to check the bot is working or not !")
	await idle()




async def start_assistant():
	""" Start assistant """
	if bot:
		await bot.start()
		log.info("Assistant activated, startup in progress . . .\n")
		load_plugins() 
	else:
		log.info("Assistant start unsuccessful, please check that you have given the bot token.\n")
		log.info("skipping assistant start !")




async def start_userbot():
	""" Start userbot """
	if app:
		await app.start()
		log.info("Userbot activated, startup in progress . . .\n")
		await load_modules()
	else:
		log.info("Userbot startup unsuccessful, please check everything again ...")
		log.info("Couldn't load modules of userbot")




async def start_bot():
	""" Main startup """
	log.info("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	log.info("initialising . . .\n\n")
	await start_assistant()
	await start_userbot()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
