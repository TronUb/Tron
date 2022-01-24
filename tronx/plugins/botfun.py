from pyrogram import filters

from tronx import app



collect = {}

numbers = [f"{x}" for x in range(10)]
cmd_handler = ["+", "-"]



@app.bot.on_message(filters.command(numbers, cmd_handler) & filters.group)
async def increment_decrement(_, m):
	reply = m.reply_to_message

	if (reply.from_user.is_self) or (reply.from_user.is_bot):
		return

	if reply:
		prefix = [x for x in m.text]
		if str(reply.from_user.id) in collect:
			if prefix[0] == "+":
				data = collect.get(str(reply.from_user.id)) 
				collect.update({str(reply.from_user.id) : str(int(data) + int(prefix[1]))})
				await app.bot.send_message(
					m.chat.id,
					f"{reply.from_user.first_name}: " + str(int(data) + int(prefix[1])) + " increment"
				)
			elif prefix[0] == "-":
				data = collect.get(str(reply.from_user.id)) 
				collect.update({str(reply.from_user.id) : str(int(data) - int(prefix[1]))})
				await app.bot.send_message(
					m.chat.id,
					f"{reply.from_user.first_name}: " + str(int(data) - int(prefix[1])) + " decrement"
				)
		elif str(reply.from_user.id) not in collect:
			if prefix[0] == "+":
				data = {str(reply.from_user.id) : str(1)}
				collect.update(data)
				await app.bot.send_message(
					m.chat.id,
					f"{reply.from_user.first_name}: 1 increment"
				) 
			elif prefix[0] == "-":
				data = {str(reply.from_user.id) : str(-1)}
				collect.update(data)
				await app.bot.send_message(
					m.chat.id,
					f"{reply.from_user.first_name}: 1 decrement"
				) 


