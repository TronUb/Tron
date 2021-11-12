import time

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	USER_NAME, 
	USER_ID, 
	CMD_HELP,
	Config,
	PREFIX,
	)

from tronx.database import (
	set_afk, 
	get_afk,
	)

from tronx.helpers import (
	error,
	send_edit,
	mymention,
	gen,
	# others
	Types, 
	get_message_type,
	get_readable_time,
	long,
	delete,
)

from tronx.database.postgres import dv_sql as dv




CMD_HELP.update(
	{"afk": (
		"afk",
		{
		"afk" : "leave your chats untouchable, stop yourself from chatting . . ."
		}
		)
	}
)




@app.on_message(gen("afk"))
async def go_offline(_, m: Message):
	try:
		start = int(time.time())
		if long(m) >= 2:
			set_afk(True, m.text.split(None, 1)[1], start) # with reason
			await send_edit(
				m, 
				"{} is now Offline.\nBecause: {}".format(mymention(), m.text.split(None, 1)[1]),
				delme=2
				)
		elif long(m) == 1 and long(m) < 4096:
			if dv.getdv("AFK_TEXT"):
				reason = dv.getdv("AFK_TEXT")
			elif Config.AFK_TEXT:
				reason = Config.AFK_TEXT
			else:
				reason = False
			if reason:
				set_afk(True, reason, start)
			elif not reason:
				set_afk(True, "", start) # without reason
			await send_edit(
				m, 
				"{} is now offline.".format(mymention()),
				delme=2
				)
	except Exception as e:
		await error(m, e)




# notify mentioned users
@app.on_message(filters.incoming & ~filters.bot & ~filters.channel, group=12)
async def offline_mention(_, m: Message):
	try:
		get = get_afk()
		if get and get["afk"]: 
			reply = m.reply_to_message
			if reply and reply.from_user.id == USER_ID:
				return

			if "-" in str(m.chat.id):
				cid = str(m.chat.id)[4:]
			else:
				cid = str(m.chat.id)

			end = int(time.time())
			otime = get_readable_time(end - get["afktime"])
			if get["reason"] and get["afktime"]:
				msg = await m.reply(
					"Sorry {} is currently offline !\n**Time:** {}\n**Because:** {}".format(mymention(), otime, get['reason'])
					)
				await delete(m, 3)
			elif get["afktime"] and not get["reason"]:
				await m.reply(
					"Sorry {} is currently offline !\n**Time:** {}".format(mymention(), otime)
					)
				await delete(m, 3)
			content, message_type = get_message_type(m)
			if message_type == Types.TEXT:
				if m.text:
					text = m.text
				else:
					text = m.caption
			else:
				text = message_type.name

			await app.send_message(
				Config.LOG_CHAT, 
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
		await error(m, e)




# come back online
@app.on_message(filters.me, group=13)
async def back_online(_, m: Message):
	try:
		# don't break afk while going offline
		if m.text:
			if m.text.startswith(f"{PREFIX}afk"):
				return
			elif "#afk" in m.text:
				return
		elif m.media:
			pass

		get = get_afk()
		if get and get['afk'] and filters.outgoing:
			end = int(time.time())
			afk_time = get_readable_time(end - get["afktime"])
			msg = await app.send_message(
				m.chat.id, 
				f"{mymention()} is now online !\n**Time:** `{afk_time}`"
				)
			set_afk(False, "", 0)
		else:
			return

	except Exception as e:
		await error(m, e)


