import asyncio

from pyrogram.types import Message

from tronx import app, gen




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
async def spam_handler(_, m: Message):
	replied = m.reply_to_message
	reply_to_id = replied.message_id if replied else ""
	if not replied and len(m.command) > 1:
		await m.delete()
		times = m.command[1]
		spam_msg = m.text.split(None, 2)[2]
		for _ in range(int(times)):
			await app.send_message(
				m.chat.id, 
				spam_msg, 
				reply_to_message_id=reply_to_id
			)
			await asyncio.sleep(0.10)
	elif replied and len(m.command) > 1:
		await m.delete()
		times = m.command[1] if m.command[1].isdigit() else 0
		spam_msg = m.reply_to_message.message_id
		for x in range(times):
			await app.copy_message(
				m.chat.id, 
				m.chat.id, 
				spam_msg
			)




@app.on_message(gen("dspam", allow = ["sudo"]))
async def delayspam_handler(_, m: Message):
	if app.long(m) < 3:
		return await app.send_edit(m, f"Use like this: `{app.MyPrefix()[0]}dspam [count spam] [delay time in seconds] [text messages]`")

	if app.long(m) > 2 and not m.reply_to_message:
		await m.delete()
		msg = m.text.split(None, 3)
		times = int(msg[1]) if msg[1].isdigit() else None
		sec = int(msg[2]) if msg[2].isdigit() else None
		text = msg[3]
		for x in range(times):
			await app.send_message(
				m.chat.id,
				text
				)
			await asyncio.sleep(sec)
	else:
		await app.send_edit(m,"Something wrong in spam command !")
