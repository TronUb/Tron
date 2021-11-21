from pyrogram import filters

from tronx import (
	bot
)

from tronx.helpers import (
	error,
)




@bot.on_message(filters.command("id"))
async def id_of_user(_, m):
	await bot.send_message(
		m.chat.id,
		f"**YOUR ID:** `{m.from_user.id}`\n**CHAT ID:** `{m.chat.id}`"
	)
