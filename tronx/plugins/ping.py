from datetime import datetime

from pyrogram import filters

from tronx import (
	bot, 
	uptime,
)




@bot.on_message(filters.command(["ping"]))
async def bot_ping(_, m):
	start = datetime.now()
	end = datetime.now()
	ms = (end - start).microseconds / 1000
	await bot.send_message(
		m.chat.id,
		f"Pong !\n`{ms}`\nUptime: `{uptime()}`",
	)








