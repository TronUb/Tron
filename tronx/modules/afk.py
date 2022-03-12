import time

from pyrogram import filters
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)





app.CMD_HELP.update(
	{"afk": (
		"afk",
		{
		"afk" : "leave your chats untouchable, stop yourself from chatting . . ."
		}
		)
	}
)





@app.on_message(gen("afk", allow = ["sudo"]), group=0)
async def go_offline(_, m: Message):
	try:
		start = int(time.time())
		if app.long(m) >= 2:
			reason = m.text.split(None, 1)[1]
			app.set_afk(True, reason, start) # with reason
			await app.send_edit(m, f"{app.UserMention()} is now Offline.\nBecause: {reason}", delme=2)

		elif app.long(m) == 1 and app.long(m) < 4096:
			if app.getdv("AFK_TEXT"):
				reason = app.getdv("AFK_TEXT")
			elif app.AFK_TEXT:
				reason = app.AFK_TEXT # config.AFK_TEXT
			else:
				reason = False

			if reason:
				app.set_afk(True, reason, start) # with reason
				await app.send_edit(m, f"{app.UserMention()} is now offline.\nBecause: {reason}", delme=2)
			else:
				app.set_afk(True, "", start) # without reason
				await app.send_edit(m, f"{app.UserMention()} is now offline.", delme=2)

	except Exception as e:
		await app.error(m, e)




# notify mentioned users
@app.on_message(~filters.bot & ~filters.channel & filters.private | filters.mentioned, group=1)
async def offline_mention(_, m: Message):
	try:
		get = app.get_afk()
		if get and get["afk"]: 
			if m.from_user.id == app.id:
				return

			if "-" in str(m.chat.id):
				cid = str(m.chat.id)[4:]
			else:
				cid = str(m.chat.id)

			end = int(time.time())
			otime = app.GetReadableTime(end - get["afktime"])
			if get["reason"] and get["afktime"]:
				msg = await app.send_message(
					m.chat.id,
					"Sorry {} is currently offline !\n**Time:** {}\n**Because:** {}".format(app.UserMention(), otime, get['reason']),
					reply_to_message_id=m.message_id
					) 
				await app.delete(msg, 3)
			elif get["afktime"] and not get["reason"]:
				msg = await app.send_message(
					m.chat.id,
					"Sorry {} is currently offline !\n**Time:** {}".format(app.UserMention(), otime),
					reply_to_message_id=m.message_id
					)
				await app.delete(msg, 3)
			content, message_type = app.GetMessageType(m)
			if message_type == app.TEXT:
				if m.text:
					text = m.text
				else:
					text = m.caption
			else:
				text = message_type.name

			await app.send_message(
				app.LOG_CHAT, 
				f"""#mention\n\n
				**User:** `{m.from_user.first_name}`\n
				**Id:** {m.from_user.id}\n
				**Group:** `{m.chat.title}`\n
				**Message:** `{text[:4096]}`\n
				[Go to message](https://t.me/c/{cid}/{m.message_id})
				""",
				parse_mode = "markdown"
				)
	except Exception as e:
		await app.error(m, e)




# come back online
@app.on_message(filters.me & ~filters.channel, group=2)
async def afkme_handler(_, m: Message):
	try:
		# don't break afk while going offline
		if m.text:
			if m.text.startswith(f"{app.PREFIX}afk"):
				return
			elif "#afk" in m.text:
				return
		elif m.media:
			pass

		get = app.get_afk()
		if get and get["afk"] and filters.outgoing:
			end = int(time.time())
			afk_time = app.GetReadableTime(end - get["afktime"])
			msg = await app.send_message(
				m.chat.id, 
				f"{app.UserMention()} is now online !\n**Offline Time:** `{afk_time}`"
			)
			app.set_afk(False, "", 0)

	except Exception as e:
		await app.error(m, e)


