import asyncio
from pyrogram import idle
from tronx.clients import app




loop = asyncio.get_event_loop()



async def start_assistant():
	"""
	this function starts the pyrogram bot client.
	"""
	if app.bot:
		await app.bot.start()
		app.log.info("Assistant activated, startup in progress . . .\n")
	else:
		app.log.info("Assistant start unsuccessful, please check that you have given the bot token.\n")
		app.log.info("skipping assistant start !")




async def start_userbot():
	"""
	this function starts the pyrogram userbot client.
	"""
	if app:
		await app.start()
		app.log.info("Userbot activated, startup in progress . . .\n")
	else:
		app.log.info("Userbot startup unsuccessful, please check everything again ...")
		app.log.info("Couldn't load modules of userbot")




async def start_bot():
	""" 
	This function uses 'start_assistant' & 'start_userbot' with 
	clients custom 'import_module' to start clients & import modules.
	"""
	print("___________________________________. Welcome to Tron corporation .___________________________________\n\n\n")
	print("PLUGINS: Installing . . .\n\n")
	plugins = app.import_module("tronx/plugins/", exclude=app.NoLoad())
	print(f"\n\n{plugins} plugins Loaded\n\n")
	print("MODULES: Installing . . .\n\n")
	modules = app.import_module("tronx/modules/", exclude=app.NoLoad())
	print(f"\n\n{modules} modules Loaded")
	await start_assistant()
	await start_userbot()
	await app.add_logbot()
	await idle() # block execution




if __name__ == '__main__':
	loop.run_until_complete(start_bot())



