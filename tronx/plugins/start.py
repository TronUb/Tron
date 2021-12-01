import time

from tronx import bot

from pyrogram import filters
from pyrogram.types import Message




@bot.on_message(filters.command("help"))
async def send_help(_, m: Message):
	await bot.send_message(
		m.chat.id,
		"How can i help you ?"
		)
