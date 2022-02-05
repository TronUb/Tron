import asyncio
from pyrogram import idle
from tronx.clients import app




loop = asyncio.get_event_loop()



async def start_assistant():
	"""assistant start in __main__"""
	if app.bot:
		await app.bot.start()
		app.log.info("Assistant activated, startup in progress . . .\n")
	else:
		app.log.info("Assistant start unsuccessful, please check that you have given the bot token.\n")
		app.log.info("skipping assistant start !")




async def start_userbot():
	"""userbot start in __main__"""
	if app:
		await app.start()
		app.log.info("Userbot activated, startup in progress . . .\n")
		print("PEERS RESOLVING: Started . . .\n\n")
		async for x in app.iter_dialogs():
			pass
		print("PEERS RESOLVE: Done . . .")
	else:
		app.log.info("Userbot startup unsuccessful, please check everything again ...")
		app.log.info("Couldn't load modules of userbot")




async def start_bot():
	""" __main__ startup """
	print("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	print("PLUGINS: Installing . . .\n\n")
	_plugs = app.import_module("tronx/plugins/", exclude=app.NoLoad())
	print(f"\n\n{_plugs} plugins Loaded\n\n")
	print("MODULES: Installing . . .\n\n")
	_mods = app.import_module("tronx/modules/", exclude=app.NoLoad())
	print(f"\n\n{_mods} modules Loaded")
	await start_assistant()
	await start_userbot()
	await idle() # block execution




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
