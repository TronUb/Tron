import time

from tronx import (
	bot,
	BOT_ID,
)

from pyrogram import filters
from pyrogram.types import Message

from tronx.helpers import error




@bot.on_message(filters.command("start"))
async def send_help(_, m: Message):
	await m.reply("How can i help you ?")



@bot.on_message(filters.new_chat_members & filters.group)
async def added_to_group_msg(_, m):
	if m.new_chat_members[0].id == BOT_ID:
		try:
			await bot.send_message(
				m.chat.id,
				"Thank You for adding me in this group !\nUse /help to know my features."
			)
		except Exception as e:
			await error(m, e)
	else:
		return
