from datetime import datetime

from pyrogram.types import Message

from tronx import app, gen




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




@app.on_message(gen(["purge", "p"], allow = ["sudo", "channel"]))
async def purge_handler(_, m:Message):
	if m.reply_to_message:
		await app.send_edit(m, "purging . . .", text_type=["mono"])

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

		await app.send_edit(m, "Deleted `{}` messages in `{}` seconds.".format(len(msg_id), sec), text_type=["mono"], delme=4)
	else:
		await app.send_edit(m, "Reply to a message to delete all messages from tagged message to bottom message.", delme=4)




@app.on_message(gen(["purgeme", "purgme", "pgm"], allow = ["sudo", "channel"]))
async def purgeme_handler(_, m:Message):
	if app.long(m) > 1:
		target = int(m.command[1]) if m.command[1].isdigit() and m.command[1] != 0 else 1
	else:
		return await app.send_edit(m, "Give me some number after command to delete messages.", text_type=["mono"], delme=4)

	start = datetime.now()
	lim = target + 1  # command msg included

	await app.send_edit(m, f"Deleting {target} messages . . .")

	msg_id = []
	msg_id.clear()

	async for x in app.iter_history(m.chat.id, limit=lim):
		msg_id.append(x.message_id)

	await app.delete_messages(m.chat.id, message_ids=msg_id[0:lim])
	sec = (datetime.now() - start).seconds

	await app.send_edit(m, "Deleted `{}` messages in `{}` seconds.".format(target, sec), text_type=["mono"], delme=4)




@app.on_message(gen("del", allow = ["sudo", "channel"]))
async def del_handler(_, m: Message):
	reply = m.reply_to_message
	msg_ids = [m.message_id, reply.message_id] if reply else [m.message_id]

	try:
		await app.delete_messages(m.chat.id, msg_ids)
	except Exception as e:
		await app.error(m, e)
