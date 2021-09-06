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




#autoblock
@app.on_message(filters.private & filters.incoming & (~filters.me & ~filters.bot), group=3)
async def auto_block(app, m: Message):
	if not Config.PMPERMIT:
		return
	elif m.from_user.is_verified:
		return
	if m.chat.type == "private":
		user_id = m.chat.id
	else:
		print("Couldn't get user id !")
		return
	guest = await app.get_users(user_id)
	try:
		if db.get_whitelist(user_id):
			return
		else:
			if db.get_msgid(user_id):
				old_msg= db.get_msgid(user_id)
				await app.delete_messages(
					chat_id=m.chat.id, 
					message_ids=old_msg
				)
			else:
				pass
			if Config.PMPERMIT_TEXT:
				msg = await app.send_message(
						m.chat.id,
						Config.PMPERMIT_TEXT,
						disable_web_page_preview=True
					)
			elif (Config.PMPERMIT_PIC) and (Config.PMPERMIT_TEXT):
				msg = await app.send_video(
					m.chat.id,
					Config.PMPERMIT_PIC,
					caption=Config.PMPERMIT_TEXT,
					disable_web_page_preview=True
				)
			else:
				print("Failed to send pmpermit warning !")
				return
			users.append(user_id)
			db.set_msgid(m.chat.id, msg.message_id)
			if m.from_user:
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



# allow 
#--------------------------------------------------------------------------------------------------------------------


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
		await send_edit(
			m, 
			f"Failed to approve [{user_name}](tg://user?id={user_id})"
			)




@app.on_message(gen(["da", "disapprove", "nopm"]))
async def revoke_pm_block(app, m:Message):
	reply = m.reply_to_message
	cmd = m.command[1]
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
	if user_name:
		db.del_whitelist(user_id)
		await send_edit(m, f"[{u_name}](tg://user?id={user_id}) has been disapproved for pm!")
		await app.send_message(
			Config.LOG_CHAT, 
			f"#disallow\n\n[{u_name}](tg://user?id={user_id}) has been disapproved for pm !"
		)
	else:
		print("Can't allow this user . . .")

                
