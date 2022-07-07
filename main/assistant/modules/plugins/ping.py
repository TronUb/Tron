from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from tronx import app



@app.bot.on_message(filters.command("ping"), group=-1)
async def bot_ping(_, m: Message):
	if not m.chat.type in ["supergroup", "group"]:
		start = datetime.now()
		end = datetime.now()
		ms = (end - start).microseconds / 1000
		await app.bot.send_message(
			m.chat.id,
			f"Pong !\n`{ms}`\nUptime: `{app.uptime()}`"
		)
	elif m.chat.type in ["supergroup", "group"]:
		start = datetime.now()
		msg = await app.bot.send_message(
			m.chat.id,
			"Pinging . . ."
		)
		end = datetime.now()
		ms = (end - start).microseconds / 1000
		await msg.edit(f"Pong !\n`{ms}`\nUptime: `{app.uptime()}`")








