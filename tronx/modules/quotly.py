import random
import asyncio

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"quotly" : (
		"quotly",
		{
		"q [reply to message]" : "Make Image Of Your Texts." 
		}
		)
	}
)



@app.on_message(gen(["q"]))
async def quote(_, m: Message):
	reply = m.reply_to_message
	if not reply:
		return await app.send_edit(m, "Reply to any users text message", delme=2)

	await app.send_edit(m, "Making a Quote . . .", mono=True)
	await reply.forward("@QuotLyBot")
	is_sticker = True
	progress = 0
	while is_sticker:
		try:
			msg = await app.get_history(
				"@QuotLyBot", 
				1
				)
			check = msg[0]["sticker"]["file_id"]
			is_sticker = False
		except:
			await asyncio.sleep(0.5)
	if msg_id := msg[0]["message_id"]:
		await asyncio.gather(
			m.delete(),
			app.copy_message(
				m.chat.id, 
				"@QuotLyBot", 
				msg_id
				)
			)
