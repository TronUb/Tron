import time

from pyrogram.types import Message
from pyrogram import filters

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
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


IgnoreChat = app.get_welcome_ids()




@app.on_message(filters.new_chat_members & filters.group & filters.chat(IgnoreChat))
async def send_welcome(_, m: Message):
	chat = app.get_welcome(str(m.chat.id))
	if bool(chat) is True:
		if chat["file_id"] is None:
			return

	try:
		file_id = chat["file_id"] if chat["file_id"] else False
		caption = chat["caption"] if chat["caption"] else False
		if file_id and not file_id.startswith("#"): # as a text
			return await app.send_message(m.chat.id, f"{file_id}", reply_to_message_id=m.message_id)

		elif file_id and file_id.startswith("#"): # as a file id 
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
				chat_id=m.chat.id,
				file_id=file_id,
				reply_to_message_id=m.message_id
			)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["setwelcome", "setwc"], allow = ["sudo", "channel"]))
async def save_welcome(_, m: Message):
	if await app.private(m):
		return

	await app.send_edit(m, "Setting this media as a welcome message . . .", mono=True)
	reply = m.reply_to_message
	if reply:
		try:
			if bool(reply.media) is True:
				fall = app.get_file_id(reply)
				file_id = fall["data"] if fall["data"] else None
				caption = fall["caption"] if fall["caption"] else None

				if caption:
					app.set_welcome(str(m.chat.id), "#" + file_id, caption)
				else:
					app.set_welcome(str(m.chat.id), "#" + file_id)
				await app.send_edit(m, "Added this media to welcome message . . .", delme=2, mono=True)
			elif bool(reply.media) is False:
				app.set_welcome(str(m.chat.id), reply.text.markdown)
				await app.send_edit(m, "Added this text to welcome message . . .", delme=2, mono=True)
		except Exception as e:
			await app.error(m, e)
			print(e)
	else:
		await app.send_edit(m, "Please reply to some media or text to set welcome message . . .", delme=2, mono=True)      




@app.on_message(gen(["delwelcome", "delwc"], allow = ["sudo", "channel"]))
async def delete_welcome(_, m: Message):
	if await app.private(m):
		return

	try:
		await app.send_edit(m, "Checking welcome message for this group . . .", mono=True)
		app.del_welcome(str(m.chat.id))
		await app.send_edit(m, "Successfully deleted welcome message for this chat . . .", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["getwelcome", "getwc"], allow = ["sudo", "channel"]))
async def delete_welcome(_, m: Message):
	if await app.private(m):
		return

	try:
		await app.send_edit(m, "Getting welcome message of this group . . .")
		data = app.get_welcome(str(m.chat.id))
		text = data["file_id"]
		cap = data["caption"]

		if text is None and cap is None :
			await app.send_edit(m, "No welcome message was assigned to this group.", mono=True, delme=3)
		elif text is not None and cap is None:
			if text.startswith("#"):
				await app.send_cached_media(
					m.chat.id,
					file_id=text.replace("#", ""),
					reply_to_message_id=m.message_id
					)
				await m.delete()
			else:
				await app.send_edit(m, text, mono=True)
		elif text is not None and cap is not None:
			if text.startswith("#"):
				await app.send_cached_media(
					m.chat.id,
					file_id=text.replace("#", ""),
					caption=cap,
					reply_to_message_id=m.message_id
					)
				await m.delete()
	except Exception as e:
		await app.error(m, e)



