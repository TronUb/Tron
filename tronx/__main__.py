import asyncio
from pyrogram import idle
from tronx.clients import app




loop = asyncio.get_event_loop()



async def start_assistant():
	""" Start assistant """
	if app.bot:
		app.log.info("Assistant activated, startup in progress . . .\n")
	else:
		app.log.info("Assistant start unsuccessful, please check that you have given the bot token.\n")
		app.log.info("skipping assistant start !")




async def start_userbot():
	""" Start userbot """
	if app:
		app.log.info("Userbot activated, startup in progress . . .\n")
	else:
		app.log.info("Userbot startup unsuccessful, please check everything again ...")
		app.log.info("Couldn't load modules of userbot")




async def start_bot():
	""" Main startup """
	print("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	print("initialising . . .\n\n")
	print("Loading plugins:\n\n")
	_plugs = app.import_module("tronx/plugins/")
	print(f"\n\n{_plugs} plugins Loaded\n\n")
	print("Loading modules:\n\n")
	_mods = app.import_module("tronx/modules/")
	print(f"\n\n{_mods} modules Loaded")
	await start_assistant()
	await start_userbot()
	idle()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
