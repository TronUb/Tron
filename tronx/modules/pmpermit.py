import os, time, asyncio

from sys import platform

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.errors import (
	PeerIdInvalid, 
	UsernameNotOccupied, 
	UsernameInvalid
)

from tronx import (
	app, 
	CMD_HELP, 
	BOT_USERNAME,
	Config,
	PREFIX
	)

from tronx.database.postgres import pmpermit_sql as db

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	mention_markdown, 
	extract_user,
)




CMD_HELP.update(
	{"pmpermit" : (
		"pmpermit",
		{
		"a" : "approve a user when pmpermit is on",
		"da" : "disapprove a user when pmpermit is on"
		}
		)
	}
)




users = []




def remove(duplicate):
	userlist = []
	for num in duplicate:
		if num not in userlist:
			userlist.append(num)
	return userlist


async def old_msg(app: Client, m: Message, user_id):
	if bool(db.get_msgid(user_id)) is True:
		old_msgs = db.get_msgid(user_id)
		await app.delete_messages(
			chat_id=m.chat.id, 
			message_ids=old_msgs
		)
	else:
		pass




#autoblock
@app.on_message(filters.private & (~filters.me & ~filters.bot), group=3)
async def auto_block(_, m: Message):
	if not Config.PMPERMIT:
		return
	if m.from_user.is_verified:
		return
	if not db.get_whitelist(user_id) is True:
		user_id = m.chat.id
		guest = await app.get_users(user_id)
		try:
			await old_msg(app, m, user_id)
			if Config.PMPERMIT_PIC:
				msg = await app.send_video(
					m.chat.id,
					Config.PMPERMIT_PIC,
					caption=Config.PMPERMIT_TEXT,
					disable_web_page_preview=True
				)
			elif not Config.PMPERMIT_PIC:
				msg = await app.send_message(
					m.chat.id,
					Config.PMPERMIT_TEXT,
					disable_web_page_preview=True
				)
			else:
				return print("The bot didn't send pmpermit warning message . . .")
			users.append(user_id)
			db.set_msgid(m.chat.id, msg.message_id)
			msg = "#pmpermit\n\n"
			msg += f"Name: `{m.from_user.first_name}`\n"
			msg += f"Id: `{m.from_user.id}`\n"
			if m.from_user.username:
				msg += f"Username: `@{m.from_user.username}`\n"
			else:
				msg += f"Username: `None`\n"
			msg += f"Message: `{m.text}`\n"
			if users.count(user_id) == Config.PM_LIMIT:
				await app.block_user(user_id)
				await app.send_message(
					Config.LOG_CHAT,
					f"{m.from_user.first_name} is now blocked !"
				)
			else:
				try:
					await app.send_message(
						Config.LOG_CHAT,
						msg
					)
				except PeerIdInvalid:
					pass
	else:
		return 
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["a", "approve", "pm"]))
async def approve_pm(app, m: Message):
	reply = m.reply_to_message
	cmd = m.command
	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and len(cmd) == 1:
			await send_edit(m, "Whom should i approve, piro ?")
		elif not reply and len(cmd) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				await send_edit(m, "Please try again later . . .")
				return
		else:
			return

	info = await app.get_users(user_id)
	user_name = info.first_name
	try:
		db.set_whitelist(user_id, True)
		await send_edit(m, f"[{user_name}](tg://user?id={user_id}) is now approved to pm.")

		list(set(users) - set([user_id]))
		if db.get_msgid(user_id):
			old_msg = db.get_msgid(user_id)
			await app.delete_messages(
				chat_id=m.chat.id,
				message_ids=old_msg
			)
		else:
			time.sleep(1)
	except Exception as e:
		await error(m, e)
		await send_edit(m, f"Failed to approve [{user_name}](tg://user?id={user_id})")




@app.on_message(gen(["da", "disapprove", "nopm"]))
async def revoke_pm_block(app, m:Message):
	reply = m.reply_to_message
	cmd = m.command
	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and len(cmd) == 1:
			await send_edit(m, "Whom should i disapprove, piro ?")
		elif not reply and len(cmd) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				await send_edit(m, "Please try again later . . .")
				return
		else:
			return

	info = await app.get_users(user_id)
	user_name = info.first_name
	if user_name:
		db.del_whitelist(user_id)
		await send_edit(m, f"[{user_name}](tg://user?id={user_id}) has been disapproved for pm!")
		await app.send_message(
			Config.LOG_CHAT, 
			f"#disallow\n\n[{user_name}](tg://user?id={user_id}) has been disapproved for pm !"
		)
	else:
		print("Can't disallow this user . . .")

                
