import os
import time
import asyncio

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

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	mention_markdown, 
	extract_user,
	long,
)

from tronx.database.postgres import dv_sql as dv

from tronx.database.postgres import pmpermit_sql as db




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




async def send_warn(app: Client, m: Message, user):
	""" Send warning messages """
	if dv.getdv("PMPERMIT_PIC"):
		pic = dv.getdv("PMPERMIT_PIC")
	elif Config.PMPERMIT_PIC:
		pic = Config.PMPERMIT_PIC
	else:
		pic = False

	if dv.getdv("PMPERMIT_TEXT"):
		text = dv.getdv("PMPERMIT_TEXT")
	elif Config.PMPERMIT_TEXT:
		text = Config.PMPERMIT_TEXT

	if pic:
		msg = await app.send_video(
			m.chat.id,
			text,
			caption=Config.PMPERMIT_TEXT,
			disable_web_page_preview=True
		)
	elif not pic:
		msg = await app.send_message(
			m.chat.id,
			text,
			disable_web_page_preview=True
			)
	else:
		return print("The bot didn't send pmpermit warning message . . .")
	db.set_msgid(user, msg.message_id)




#autoblock
@app.on_message(filters.private & filters.incoming & (~filters.me & ~filters.bot), group=3)
async def auto_block(_, m: Message):
	if bool(dv.getdv("PMPERMIT")) is False:
		return
	if m.from_user.is_verified:
		return
	if bool(db.get_whitelist(m.chat.id)) is False:
		user = await app.get_users(m.chat.id)
	else:
		return

	if dv.getdv("PM_LIMIT"):
		pmlimit = int(dv.getdv("PM_LIMIT"))
	if Config.PM_LIMIT:
		pmlimit = int(Config.PM_LIMIT)

	# log user info to log chat

	msg = "#pmpermit\n\n"
	msg += f"Name: `{user.first_name}`\n"
	msg += f"Id: `{user.id}`\n"
	if user.username:
		msg += f"Username: `@{user.username}`\n"
	else:
		msg += f"Username: `None`\n"
	msg += f"Message: `{m.text}`\n"

	if bool(db.get_warn(user.id)) is False:
		db.set_warn(user.id, 1)
		await send_warn(app, m, user.id)

	elif bool(db.get_warn(user.id)) is True:
		warn = int(db.get_warn(user.id))
		if warn < pmlimit:
			maximum = warn + 1
			db.set_warn(user.id, maximum)
			await old_msg(app, m, user.id) # delete old warns
			await send_warn(app, m, user.id) # send new warns
		elif warn >= pmlimit:
			done = await app.block_user(user.id)
			if done:
				try:
					await app.send_message(
						Config.LOG_CHAT,
						f"{user.first_name} is now blocked for spamming !"
					)
				except PeerIdInvalid:
					pass
			else:
				print("Failed to block user because of spamming in pm")
		else:
			print("Can't block user in pm")




@app.on_message(gen(["a", "approve"]))
async def approve_pm(app, m: Message):
	reply = m.reply_to_message
	cmd = m.command
	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and long(m) == 1:
			await send_edit(m, "Whom should i approve, piro ?", delme=3)
			return
		elif not reply and long(m) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				await send_edit(m, "Please try again later . . .", delme=3)
				return
		else:
			await send_edit(m, "Failed to approve user . . .", delme=2)
			return

	info = await app.get_users(user_id)
	user_name = info.first_name
	try:
		db.set_whitelist(user_id, True)
		await send_edit(m, f"[{user_name}](tg://user?id={user_id}) is now approved to pm.")

		db.del_warn(user_id)

		if db.get_msgid(user_id):
			await old_msg(app, m, user_id)
		else:
			pass
	except Exception as e:
		await error(m, e)
		await send_edit(m, f"Failed to approve [{user_name}](tg://user?id={user_id})")




@app.on_message(gen(["da", "disapprove"]))
async def revoke_pm_block(_, m:Message):
	reply = m.reply_to_message
	cmd = m.command
	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and long(m) == 1:
			await send_edit(m, "Whom should i disapprove, piro ?", delme=3)
		elif not reply and long(m) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				await send_edit(m, "Please try again later . . .", delme=3)
				return
		else:
			return

	info = await app.get_users(user_id)
	user_name = info.first_name
	if user_name:
		db.del_whitelist(user_id)
		await send_edit(m, f"[{user_name}](tg://user?id={user_id}) has been disapproved for pm!")
		try:
			await app.send_message(
				Config.LOG_CHAT, 
				f"#disallow\n\n[{user_name}](tg://user?id={user_id}) has been disapproved for pm !"
			)
		except Exception as e:
			print(e)
	else:
		print("Can't disallow this user . . .", delme=3)

                
