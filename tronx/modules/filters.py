import time

from pyrogram.types import Message
from pyrogram import filters

from tronx import (
	app,
	LOG_CHAT,	
)

from tronx.database.postgres import filters_sql as df  

from tronx.helpers import (
	send_edit,
	error,
	gen,
	long,
	private,
)

from . import get_file_id




@app.on_message(filters.group)
async def send_welcome(_, m: Message):
	if m.chat.type == "supergroup":
		pass
	else:
		return

	if m.from_user:
		if m.text:
			if df.get_filter(m.text)["trigger"] is not None:
				data = df.get_filter(m.text)

				if data["chat_id"] == str(m.chat.id):
					pass
				else:
					return

			else:
				return

		else:
			return

	else:
		return

	try:
		trigger = data["trigger"] if data["trigger"] else False
		file_id = data["file_id"] if data["file_id"] else False
		chat_id = data["chat_id"] if data["chat_id"] else False
		caption = data["caption"] if data["caption"] else False

		if file_id and not file_id.startswith("#"):
			await app.send_message(
				m.chat.id, 
				file_id
				)
			return
		elif file_id and file_id.startswith("#"):
			file_id = file_id.replace("#", "")
			if caption:
				await app.send_cached_media(
					chat_id=chat_id,
					file_id=file_id,
					caption=caption,
					reply_to_message_id=m.from_user.id
				)
			elif not caption:
				await app.send_cached_media(
					chat_id=chat_id,
					file_id=file_id,
					reply_to_message_id=m.from_user.id
				)
	except Exception as e:
		await error(m, e)
		print(e)




@app.on_message(gen("filter"))
async def save_welcome(_, m: Message):
	await private(m)
	await send_edit(m, "Setting this media as a . . .")
	reply = m.reply_to_message
	if reply:
		if long(m) > 1:
			pass
			cmd = m.command
		else:
			await send_edit(m, "Please give me the filter name . . .")
			return
		fall = get_file_id(m)
		file_id = fall["data"] if fall["data"] else False
		caption = fall["text"] if fall["text"] else False

		if bool(reply.media) is True:
				if caption:
					df.set_filter(chat_id=str(m.chat.id), file_id="#" + file_id, trigger=cmd[1], caption=caption)
				else:
					df.set_filter(chat_id=str(m.chat.id), file_id="#" + file_id, trigger=cmd[1], caption=False)
		else:
			await send_edit(m, "Reply to media only . . .")

		await send_edit(m, f"Added `{cmd[1]}` as a filter trigger to replied media/text . . .", delme=2)
	else:
		await send_edit(m, "Please reply to some media or text with filter name to set filter . . .", delme=2)      




@app.on_message(gen("delfilter"))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		if long(m) > 1:
			cmd = str(m.command)
		else:
			await send_edit(m, "Give me the filter name, piro !")
		await send_edit(m, "Checking existence of filter . . .")
		df.del_filter(cmd[1])
		await send_edit(m, f"Successfully deleted `{cmd[1]}` for this chat . . .", delme=2)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("filters"))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		if long(m) > 1:
			cmd = m.command
			if cmd[1].isdigit():
				cmd = str(cmd)

		else:
			await send_edit(m, "Give me the filter name, piro !")
			return
		await send_edit(m, "Getting filter . . .")
		data = df.get_filter(cmd[1])
		await send_edit(m, data)
	except Exception as e:
		await error(m, e)



