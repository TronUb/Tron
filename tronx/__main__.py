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
	get_self, 
	get_bot,
	add_user,
	userlise,
)




loop = asyncio.get_event_loop()




def load_plugins():
	""" Assistant modules """
	from tronx.plugins import PLUGINS
	print("Loading plugins of [ assistant ], Please wait...\n")
	for plug in PLUGINS:
		importlib.import_module("tronx.plugins." + plug)

	print("-----------------------")
	print("List of Plugins:\n\n")
	for x in PLUGINS:
		print(x + " Loaded !")
	num_plug = len(PLUGINS)
	print(f"\nTotal {num_plug} Plugins Loaded !")
	print("-----------------------\n\n")




async def load_modules():
	""" Userbot modules """
	from tronx.modules import MODULES

	print("Loading modules of [ Userbot ], Please wait ...\n")
	for plug in MODULES:
		importlib.import_module("tronx.modules." + plug)

	print("-----------------------")
	print("List Of Modules:\n\n")
	for y in MODULES:
		print(y + " Loaded !")
	num_mod = len(MODULES)
	print(f"\nTotal {num_mod} Modules Loaded !")
	print("-----------------------\n\n")
	print("Try .ping or .alive to check the bot is working or not !")
	await idle()




async def start_assistant():
	""" Start assistant """
	if bot:
		await bot.start()
		print("Assistant activated, startup in progress . . .\n")
		load_plugins() 
	else:
		print("Assistant start unsuccessful, please check that you have given the bot token.\n")
		print("skipping assistant start !")




async def start_userbot():
	""" Start userbot """
	if app:
		await app.start()
		print("Userbot activated, startup in progress . . .\n")
		await load_modules()
	else:
		print("Userbot startup unsuccessful, please check everything again ...")
		print("Couldn't load modules of userbot")




async def start_bot():
	""" Main startup """
	print("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	print("initialising . . .\n\n")
	await userlise() # first startup
	await start_assistant()
	await start_userbot()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
