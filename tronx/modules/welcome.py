import time

from pyrogram.types import Message
from pyrogram import filters

from tronx import (
	app,
	LOG_CHAT,
	CMD_HELP,
)

from tronx.database.postgres import welcome_sql as dw   

from tronx.helpers import (
	send_edit,
	error,
	gen,
	long,
	private,
)

from . import get_file_id




CMD_HELP.update(
	{"welcome": (
		"welcome",
		{
		"setwc [reply to media/text]" : "Set welcome message for group.",
		"getwc" : "Use it in group to get saved welcome message.",
		"delwc" : "Use it in group to delete saved welcome message.",
		}
		)
	}
)




@app.on_message(filters.new_chat_members & filters.group)
async def send_welcome(_, m: Message):
	chat = dw.get_welcome(str(m.chat.id))
	if bool(chat) is True:
		if chat["file_id"] is None:
			return

	try:
		file_id = chat["file_id"] if chat["file_id"] else False
		caption = chat["caption"] if chat["caption"] else False
		if file_id and not file_id.startswith("#"):
			return await app.send_message(m.chat.id, f"{file_id}, reply_to_message_id=m.message_id)

		elif file_id and file_id.startswith("#"):
			file_id = file_id.replace("#", "")
		if caption:
			await app.send_cached_media(
				m.chat.id,
				file_id=file_id,
				caption=f"{caption}",
				reply_to_message_id=m.message_id
			)
		elif not caption:
			await app.send_cached_media(
				m.chat.id,
				file_id=file_id,
				reply_to_message_id=m.message_id
			)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["setwelcome", "setwc"]))
async def save_welcome(_, m: Message):
	await private(m)
	await send_edit(m, "Setting this media as a welcome message . . .", mono=True)
	reply = m.reply_to_message
	if reply:
		try:
			fall = get_file_id(m)
			file_id = fall["data"] if fall["data"] else None
			caption = fall["caption"] if fall["caption"] else None

			if bool(reply.media) is True:
				if caption:
					dw.set_welcome(str(m.chat.id), "#" + file_id, caption)
				else:
					dw.set_welcome(str(m.chat.id), "#" + file_id)
				await send_edit(m, "Added this media to welcome message . . .", delme=2, mono=True)
			elif bool(reply.media) is False:
				dw.set_welcome(str(m.chat.id), reply.text)
				await send_edit(m, "Added this text to welcome message . . .", delme=2, mono=True)
		except Exception as e:
			await error(m, e)
			print(e)
	else:
		await send_edit(m, "Please reply to some media or text to set welcome message . . .", delme=2, mono=True)      




@app.on_message(gen(["delwelcome", "delwc"]))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		await send_edit(m, "Checking welcome message for this group . . .", mono=True)
		dw.del_welcome(str(m.chat.id))
		await send_edit(m, "Successfully deleted welcome message for this chat . . .", delme=2, mono=True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["getwelcome", "getwc"]))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		await send_edit(m, "Getting welcome message of this group . . .")
		data = dw.get_welcome(str(m.chat.id))
		text = data["file_id"]
		cap = data["caption"]

		if text is None and cap is None :
			await send_edit(m, "No welcome message was assigned to this group.", mono=True, delme=3)
		elif text is not None and cap is None:
			if text.startswith("#"):
				await app.send_cached_media(
					m.chat.id,
					file_id=text,
					reply_to_message_id=m.message_id
					)
				await m.delete()
			else:
				await send_edit(m, text, mono=True)
		elif text is not None and cap is not None:
			if text.startswith("#"):
				await app.send_cached_media(
					m.chat.id,
					file_id=text,
					caption=cap,
					reply_to_message_id=m.message_id
					)
				await m.delete()
	except Exception as e:
		print(e)
		await error(m, e)



