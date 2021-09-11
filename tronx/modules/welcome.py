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
)




@app.on_message(filters.new_chat_members)
async def send_welcome(_, m: Message):
	if str(m.chat.id).startswith("-100"):
		chat_id = str(m.chat.id)[4:]
	else:
		chat_id = m.chat.id
	if bool(dw.get_welcome(chat_id)) is True:
		media_id = dw.get_welcome(chat_id)
		try:
			app.send_cached_media(
				m.chat.id,
				file_id=media_id
				)
		except:
			await send_edit(m, media_id)
	elif bool(dw.get_welcome(chat_id) is False:
		return




@app.on_message(gen("setwelcome"))
async def save_welcome(_, m: Message):
	reply = m.reply_to_message
	if reply:
		try:
			if str(m.chat.id).startswith("-100"):
				chat_id = str(m.chat.id)[4:]
			else:
				chat_id = m.chat.id
			dw.set_welcome(int(chat_id), types(m))
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Please reply to some media or text to set welcome . . .")      




@app.on_message(gen("delwelcome"))
async def delete_welcome(_, m: Message):
	try:
		dw.del_welcome(m.chat.id)
	except Exception as e:
		await error(m, e)