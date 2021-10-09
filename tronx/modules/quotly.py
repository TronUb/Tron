import random
import asyncio

from asyncio import sleep

from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
)




CMD_HELP.update(
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
		return await send_edit(m, "Reply to any users text message", delme=2)

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
			await sleep(0.5)
	await send_edit(m, "Making a Quote . . .", mono=True)
	if msg_id := msg[0]["message_id"]:
		await asyncio.gather(
			m.delete(),
			app.forward_messages(
				m.chat.id, 
				"@QuotLyBot", 
				msg_id
				)
			)
