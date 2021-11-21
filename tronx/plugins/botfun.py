from pyrogram import filters

from tronx import (
	bot,
)

from tronx.helpers import (
	long,
)


collect = {}



@bot.on_message(filters.command("1", "+") & filters.group)
async def increment(_, m):
	reply = m.reply_to_message
	if reply:
		if str(reply.from_user.id) in collect:
			data = collect.get(str(reply.from_user.id)) 
			collect.update({str(reply.from_user.id) : str(int(data) + 1)})
			await bot.send_message(
				m.chat.id,
				f"{reply.from_user.first_name}: " + str(int(data)+1) + " increment"
			)
		elif str(reply.from_user.id) not in collect:
			data = {str(reply.from_user.id) : str(1)}
			collect.update(data)
			await bot.send_message(
				m.chat.id,
				f"{reply.from_user.first_name}: 1 increment"
			) 




@bot.on_message(filters.command("1", "-") & filters.group)
async def increment(_, m):
	reply = m.reply_to_message
	if reply:
		if str(reply.from_user.id) in collect:
			data = collect.get(str(reply.from_user.id)) 
			collect.update({str(reply.from_user.id) : str(int(data) - 1)})
			await bot.send_message(
				m.chat.id,
				f"{reply.from_user.first_name}: " + str(int(data) - 1) + " increment"
			)
		elif str(reply.from_user.id) not in collect:
			data = {str(reply.from_user.id) : str(1)}
			collect.update(data)
			await bot.send_message(
				m.chat.id,
				f"{reply.from_user.first_name}: 0 increment"
			) 
