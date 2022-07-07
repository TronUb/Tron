from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from main.assistant.client import bot





@bot.on_message(filters.command("ping"), group=-1)
async def bot_ping(_, m: Message):
	if not m.chat.type in ["supergroup", "group"]:
		start = datetime.now()
		end = datetime.now()
		ms = (end - start).microseconds / 1000
		await bot.send_message(
			m.chat.id,
			f"Pong !\n`{ms}`\nUptime: `{bot.uptime()}`"
		)
	elif m.chat.type in ["supergroup", "group"]:
		start = datetime.now()
		msg = await bot.send_message(
			m.chat.id,
			"Pinging . . ."
		)
		end = datetime.now()
		ms = (end - start).microseconds / 1000
		await msg.edit(f"Pong !\n`{ms}`\nUptime: `{bot.uptime()}`")








