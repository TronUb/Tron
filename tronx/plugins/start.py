import time

from tronx import bot

from pyrogram import filters
from pyrogram.types import Message




@bot.on_message(filters.command("start"))
async def send_help(_, m: Message):
	await bot.reply("How can i help you ?")
