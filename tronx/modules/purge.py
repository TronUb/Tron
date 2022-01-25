from datetime import datetime

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
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




@app.on_message(gen(["purge", "p"], allow_channel=True))
async def purge_all(app, m:Message):
	if m.reply_to_message:
		await app.send_edit(m, "purging . . .", mono=True)

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

		await app.send_edit(m, "Deleted {} messages in {} seconds.".format(len(msg_id), sec), mono=True, delme=2)
	else:
		await app.send_edit(m, "Reply to a message to delete all from up to bottom", delme=2)




@app.on_message(gen(["purgeme", "pgm"]))
async def purge_myself(app, m:Message):
	if app.long(m) > 1:
		if m.command[1].isdigit() is False:
			return await app.send_edit(m, "Is that a number ? please give me a number . . .", mono=True)
		target = int(m.command[1])
	else:
		return await app.send_edit(m, "Give me some number after command to delete messages . . .", delme=2, mono=True)

	start = datetime.now()
	lim = target + 1  # command msg including

	await app.send_edit(m, f"Deleting {target} messages . . .")

	msg_id = []
	msg_id.clear()

	async for x in app.iter_history(m.chat.id, limit=lim):
		msg_id.append(x.message_id)

	await app.delete_messages(m.chat.id, message_ids=msg_id[0:lim])
	sec = (datetime.now() - start).seconds

	await app.send_edit(m, "Deleted {} messages in {} seconds".format(target, sec), mono=True, delme=3)




@app.on_message(gen("del"))
async def delete_tag(_, m: Message):
	reply = m.reply_to_message

	msg_id = [m.message_id, reply.message_id if reply else ""]

	try:
		await app.delete_messages(m.chat.id, msg_id)
	except Exception as e:
		await app.error(m, e)
