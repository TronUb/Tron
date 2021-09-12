import time

from pyrogram.types import Message
from pyrogram import filters

from tronx import (
	app,
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






@app.on_message(filters.new_chat_members & filters.group)
async def send_welcome(_, m: Message):
	if bool(dw.get_welcome(str(m.chat.id))) is True:
		if filters.chat(int(dw.get_welcome(str(m.chat.id))))
			pass
		else:
			return
		media_id = dw.get_welcome(str(m.chat.id))
		try:
			file_id = media_id["file_id"] if media_id["file_id"] else False
			caption = media_id["caption"] if media_id["caption"] else False
			if caption:
				await app.send_cached_media(
					m.chat.id,
					file_id=file_id,
					caption=caption,
					reply_to_message_id=m.from_user.id
				)
			elif not caption:
				await app.send_cached_media(
					m.chat.id,
					file_id=file_id,
					reply_to_message_id=m.from_user.id
				)
		except:
			await print(media_id)
	elif bool(dw.get_welcome(str(m.chat.id))) is False:
		return




@app.on_message(gen("setwelcome"))
async def save_welcome(_, m: Message):
	await private(m)
	await send_edit(m, "Setting this media as a welcome message . . .")
	reply = m.reply_to_message
	if reply:
		try:
			fall = get_file_id(m)
			file_id = fall["data"] if fall["data"] else None
			caption = fall["text"] if fall["text"] else None

			if caption:
				dw.set_welcome(str(m.chat.id), file_id, caption)
			else:
				dw.set_welcome(str(m.chat.id), file_id)
			await send_edit(m, "Added this media/text to welcome message . . .", delme=2)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Please reply to some media or text to set welcome . . .", delme=2)      




@app.on_message(gen("delwelcome"))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		await send_edit(m, "Checking welcome message . . .")
		dw.del_welcome(str(m.chat.id))
		await send_edit(m, "Successfully deleted welcome message for this chat . . .", delme=2)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("getwelcome"))
async def delete_welcome(_, m: Message):
	await private(m)
	try:
		await send_edit(m, "Getting welcome message . . .")
		data = dw.get_welcome(str(m.chat.id))
		await send_edit(m, data)
	except Exception as e:
		await error(m, e)



