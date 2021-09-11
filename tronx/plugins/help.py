import time

from tronx import bot

from pyrogram import filters
from pyrogram.types import Message




@bot.on_message(filters.command("help"))
async def send_help(_, m: Message):
	if m.from_user:
		await bot.send_message(
			m.chat.id,
			"Just use the /start command . . . 🤭"
			)
	else:
		return