from pyrogram import filters

from tronx import (
	bot,
)

from tronx.helpers import (
	long,
)




@bot.on_message(filters.command("1", "+"))
async def increment(_, m):
	reply = m.reply_to_message
	if reply:
		await bot.send_message(
			m.chat.id,
			f"{reply.from_user.first_name}: 1 increment"
		) 
