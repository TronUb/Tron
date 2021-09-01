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

from . import SUDO_USERS

from tronx.helpers import (
	error,
	send_edit,
	mymention,
	gen,
	# others
	escape_markdown,
	mention_markdown,
	Types, 
	get_message_type,
	get_readable_time,
)




CMD_HELP.update(
	{"afk": (
		"afk",
		{
		"afk" : "leave your chats untouchable, stop yourself from chatting . . ."
		}
		)
	}
)




# mentioned users
MENTIONED = []

# restricted users
AFK_RESTRICT = {}

# a delay for restricted users
DELAY_TIME = 60 # seconds

# stored time
AFK_TIME = []




@app.on_message(gen("afk") & filters.user(SUDO_USERS))
async def go_offline(_, m: Message):
	if len(m.text.split()) >= 2:
		try:
			start = int(time.time())
			set_afk(True, m.text.split(None, 1)[1], start) # with reason
			AFK_TIME.append(start)
			await send_edit(
				m, 
				"{} is now Offline.\nBecause: {}".format(mymention(), m.text.split(None, 1)[1]))
			AFK_TIME.clear()
		except Exception as e:
			await error(m, e)
	else:
		try:
			start = int(time.time())
			set_afk(True, "", start) # without reason
			AFK_TIME.append(start)
			AFK_TIME.clear()
			await send_edit(
				m, 
				"{} is now offline.".format(mymention())
				)
		except Exception as e:
			await error(m, e)




# notify mentioned users
@app.on_message(filters.mentioned & filters.incoming & ~filters.chat(str(Config.LOG_CHAT)) & ~filters.bot, group=12)
async def offline_mention(app, m: Message):
	try:
		if m.chat.id == Config.LOG_CHAT:
			return
		global MENTIONED
		get = get_afk()
		if get and get["afk"]: 
			if "-" in str(m.chat.id):
				cid = str(m.chat.id)[4:]
			else:
				cid = str(m.chat.id)
			if cid == AFK_RESTRICT:
				return
			end = int(time.time())
			otime = get_readable_time(end - get["afktime"])
			if get["reason"] and get["afktime"]:
				if m.from_user.id in MENTIONED:
					return
				await m.reply(
					"Sorry {} is currently offline !\n**Time:** {}\n**Because:** {}".format(mymention(), otime, get['reason'])
					)
			elif get["afktime"] and not get["reason"]:
				if m.from_user.id in MENTIONED:
					return
				await m.reply(
					"Sorry {} is currently offline !\n**Time:** {}".format(mymention(), otime)
					)
			content, message_type = get_message_type(m)
			if message_type == Types.TEXT:
				if m.text:
					text = m.text
				else:
					text = m.caption
			else:
				text = message_type.name
			MENTIONED.append(
				{
					"user": m.from_user.first_name, 
					"user_id": m.from_user.id, 
					"chat": m.chat.title, 
					"chat_id": cid, 
					"text": text, 
					"message_id": m.message_id
				}
				)
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
@app.on_message(filters.me & ~filters.chat(Config.LOG_CHAT), group=13)
async def back_online(app, m: Message):
	try:
		# don't break afk while going offline
		if m.text:
			if m.text.startswith(f"{PREFIX}afk") or m.text.startswith("brb"):
				return
		elif m.media:
			return

		get = get_afk()
		if get and get['afk'] and filters.outgoing:
			end = int(time.time())
			afk_time = get_readable_time(end - get["afktime"])
			await app.send_message(
				m.chat.id, 
				f"{mymention()} is now online !\n**Time:** `{afk_time}`"
				)
			set_afk(False, "", 0)
			AFK_TIME.clear()
		else:
			return

	except Exception as e:
		await error(m, e)


