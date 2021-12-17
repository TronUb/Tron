
import asyncio

from pyrogram import idle
from tronx.client import (
	app, 
	bot,
	log,
)




loop = asyncio.get_event_loop()


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
	await start_assistant()
	await start_userbot()
	await idle()




if __name__ == '__main__':
	""" Run as __main__.py """
	loop.run_until_complete(start_bot())
