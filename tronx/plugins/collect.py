import os

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

from tronx import (
	bot, 
	app,
	Config,
)

from tronx.helpers import mention_markdown  



@bot.on_message(filters.incoming)
async def collect_users_data(_, m: Message):
	if m.from_user:
		try:
			data = f"{mention_markdown(m.from_user.id, m.from_user.first_name)} "
			data += f"Started your bot."

			await app.send_message(LOG_CHAT, data) 
		except PeerIdInvalid:
			pass
	else:
		return