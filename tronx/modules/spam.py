import asyncio

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"spam" : (
		"spam",
		{
		"spam [number] [text]" : "You Know The Use Of This Command.", 
		"dspam [delay] [count] [msg]" : "Delay spam use it to spam with a delay between spamming msg."
		}
		)
	}
)




@app.on_message(gen("spam", allow = ["sudo"]))
async def spam(_, m: Message):
	replied = m.reply_to_message
	reply_to_id = replied.message_id if replied else ""
	if not replied and len(m.command) > 1:
		await m.delete()
		times = m.command[1]
		to_spam = " ".join(m.command[2:])
		if m.chat.type in ["supergroup", "group"]:
			for _ in range(int(times)):
				await app.send_message(
					m.chat.id, 
					to_spam, 
					reply_to_message_id=reply_to_id
				)
				await asyncio.sleep(0.20)
		elif m.chat.type == "private":
			await m.delete()
			for _ in range(int(times)):
				await app.send_message(
					m.chat.id, 
					to_spam
					)
				await asyncio.sleep(0.20)
	elif replied and len(m.command) > 1:
		await m.delete()
		times = m.command[1]
		print(f"{times} messages will be sent")
		cont = m.reply_to_message.message_id
		if m.chat.type in ["supergroup", "group", "private"]:
			for x in range(int(times)):
				await app.copy_message(
					m.chat.id, 
					m.chat.id, 
					m.reply_to_message.message_id
					)
		else:
			return




@app.on_message(gen("dspam", allow = ["sudo"]))
async def delay_spam(_, m: Message):
	if len(m.command) > 2 and not m.reply_to_message:
		await m.delete()
		msg = m.text.split(None, 3)
		sec = int(msg[1])
		times = int(msg[2])
		text = msg[3]
		for x in range(times):
			await app.send_message(
				m.chat.id,
				text
				)
			await asyncio.sleep(sec)
	else:
		await app.send_edit(m,"Something wrong in spam command !")
