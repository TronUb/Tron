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
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	get_readable_time,
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
		await send_edit(
			m, 
			"purging..."
			)
		start_t = datetime.now()
		user_id = None
		from_user = None
		start_message = m.reply_to_message.message_id
		end_message = m.message_id
		list_of_messages = await app.get_messages(chat_id=m.chat.id,
													message_ids=range(start_message, end_message),
													replies=0)
		del_msg = []
		purge_count = 0
		for msg in list_of_messages:
			if len(del_msg) == 100:
				await app.delete_messages(chat_id=m.chat.id,
											message_ids=del_msg,
											revoke=True)
				purge_count += len(del_msg)
				del_msg = []
			if from_user is not None:
				if msg.from_user == from_user:
					del_msg.append(msg.message_id)
			else:
				del_msg.append(msg.message_id)
		await app.delete_messages(chat_id=m.chat.id,
									message_ids=del_msg,
									revoke=True)
		purge_count += len(del_msg)
		end_t = datetime.now()
		time_taken_s = (end_t - start_t).seconds
		await m.delete()
	else:
		await send_edit(
			m, 
			"Reply to a message to delete all from up to bottom"
			)
		time.sleep(2.5)
		await m.delete()




@app.on_message(gen(["purgeme", "prm"]))
async def purge_myself(app, m:Message):
	if len(m.text.split()) >= 2 and m.text.split()[1].isdigit():
		target = int(m.text.split()[1])
	else:
		await send_edit(
			m, 
			"Give some number after to delete messages ..."
			)
	lim = target if target < 101 else 100
	get_msg = await app.get_history(m.chat.id, limit=lim) # max 100 messages
	listall = []
	counter = 0
	for x in get_msg:
		if counter == target + 1:
			break
		myself = await app.get_me()
		if x.from_user.id == int(myself.id):
			listall.append(x.message_id)
			counter += 1
	if len(listall) >= 101:
		total = len(listall)
		one = 0
		two = 0
		await m.edit("Purging ...")
		for x in range(math.ceil(len(listall) / 100)):
			if total >= 101:
				two += 100
				await app.delete_messages(
					m.chat.id, 
					message_ids=one[one:two]
					)
				one += 100
				total -= 100
			else:
				two += total
				await app.delete_messages(
					m.chat.id, 
					message_ids=one[one:two])
				one += total
				total -= total
	else:
		await app.delete_messages(
			m.chat.id, 
			message_ids=listall
			)




@app.on_message(gen("del"))
async def delete_tag(app, m:Message):
	try:
		msg_ids = [m.message_id]
		if m.reply_to_message:
			msg_ids.append(m.reply_to_message.message_id)
		await app.delete_messages(
			m.chat.id, 
			msg_ids
			)
	except Exception as e:
		await app.send_message(
			Config.LOG_CHAT,
			f"#error:\n\n{e}"
			)
		await send_edit(
			m, 
			"Check this error in your log chat."
			)
