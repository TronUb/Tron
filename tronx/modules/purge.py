import time
import math
import asyncio

from sys import platform
from datetime import datetime
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_ID
)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	get_readable_time,
	long,
)




CMD_HELP.update(
	{"purge" : (
		"purge",
		{
		"purge [tag a message]" : "Delete All Your Messages From A Fixed Point.",
		"del [reply to message]" : "Delete Your Single Selected/Tagged Message.",
		"purgeme [number]" : "Delete Your Messages In Count Numbers."
		}
		)
	}
)




@app.on_message(gen(["purge", "p"]))
async def purge_all(app, m:Message):
	if m.reply_to_message:
		await send_edit(m, "purging . . .", mono=True)

		start = datetime.now()

		messages = await app.get_messages(
			m.chat.id,
			range(m.reply_to_message.message_id, m.message_id),
			replies=0
		)

		msg_id = []
		msg_id.clear()

		for x in messages:
			msg_id.append(x.message_id)

		await app.delete_messages(
			m.chat.id,
			msg_id
			)

		end = datetime.now()
		sec = (end - start).seconds

		await send_edit(m, "Deleted {} messages in {} seconds.".format(len(msg_id), sec), mono=True, delme=2)
	else:
		await send_edit(m, "Reply to a message to delete all from up to bottom", delme=2)




@app.on_message(gen(["purgeme", "pgm"]))
async def purge_myself(app, m:Message):
	if long(m) > 1:
		if m.command[1].isdigit() is False:
			return await send_edit(m, "Is that a number ? please give me a number . . .", mono=True)
		target = int(m.command[1])
	else:
		return await send_edit(m, "Give me some number after command to delete messages . . .", delme=2, mono=True)

	start = datetime.now()
	lim = target + 1 if target <= 100 else 101 # + command message

	await send_edit(m, f"Deleting {target} messages . . .")

	msg_id = []
	msg_id.clear()

	data = await app.get_history(m.chat.id, limit=lim) 

	for x in data:
		msg_id.append(x.message_id)

	await app.delete_messages(m.chat.id, message_ids=msg_id[0:lim])
	sec = (datetime.now() - start).seconds

	await send_edit(m, "Deleted {} messages in {} seconds".format(target, sec), mono=True, delme=3)




@app.on_message(gen("del"))
async def delete_tag(_, m: Message):
	reply = m.reply_to_message
	

	msg_id = [m.message_id, reply.message_id if reply.from_user.id == USER_ID else ""] if reply else m.message_id

	try:
		await app.delete_messages(m.chat.id, msg_id)
	except Exception as e:
		await error(m, e)
