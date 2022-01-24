from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import (
	PeerIdInvalid, 
	UsernameNotOccupied, 
	UsernameInvalid
)

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"pmpermit" : (
		"pmpermit",
		{
		"a" : "approve a user when pmpermit is on",
		"da" : "disapprove a user when pmpermit is on"
		}
		)
	}
)




async def old_msg(m: Message, user_id):
	if bool(app.get_msgid(user_id)) is True:
		old_msgs = app.get_msgid(user_id)
		await app.delete_messages(
			chat_id=m.chat.id, 
			message_ids=old_msgs
		)
	else:
		pass




async def send_warn(m: Message, user):
	""" Send warning messages """
	pic = app.getdv("PMPERMIT_PIC") if bool(app.getdv("PMPERMIT_PIC")) else app.PMPERMIT_PIC if bool(app.PMPERMIT_PIC) else False

	text = app.getdv("PMPERMIT_TEXT") if bool(app.getdv("PMPERMIT_TEXT")) else app.PMPERMIT_TEXT if bool(app.PMPERMIT_TEXT) else None

	if pic:
		msg = await app.send_video(
			m.chat.id,
			pic,
			caption=text,
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
	app.set_msgid(user, msg.message_id)





# incoming autoblock
@app.on_message(filters.private & filters.incoming & (~filters.me & ~filters.bot), group=3)
async def auto_block(_, m: Message):
	if bool(app.getdv("PMPERMIT")) is False or m.from_user.is_verified:
		return

	if bool(app.get_whitelist(m.chat.id)) is False:
		user = await app.get_users(m.chat.id)
	else:
		return

	# auto allow while outgoing first msg of ub owner

	if (await app.get_history(m.chat.id, reverse=True))[0].from_user.is_self:
		return app.set_whitelist(user.id, True)

	pmlimit = app.getdv("PM_LIMIT") if app.getdv("PM_LIMIT") else int(app.PM_LIMIT) if app.PM_LIMIT else 4 

	# log user info to log chat

	msg = "#pmpermit\n\n"
	msg += f"Name: `{user.first_name}`\n"
	msg += f"Id: `{user.id}`\n"
	msg += f"Username: `@{user.username}`\n" if user.username else f"Username: `None`\n"
	msg += f"Message: `{m.text}`\n"

	warns = bool(app.get_warn(user.id))

	if warns is False:
		app.set_warn(user.id, 1)
		await send_warn(m, user.id)

	elif warns is True:
		warn = int(app.get_warn(user.id))
		if warn < pmlimit:
			maximum = warn + 1
			app.set_warn(user.id, maximum)
			await old_msg(m, user.id) # delete old warns
			await send_warn(m, user.id) # send new warns
		elif warn >= pmlimit:
			done = await app.block_user(user.id)
			if done:
				try:
					await app.send_message(
						app.LOG_CHAT,
						f"{user.first_name} is now blocked for spamming !"
					)
				except PeerIdInvalid:
					pass
			else:
				await app.send_edit(m, "Failed to block user because of spamming in pm", mono=True)
		else:
			print("Something went wrong in pmpermit")




@app.on_message(gen(["a", "approve"]))
async def approve_pm(app, m: Message):
	if m.chat.type == "bot":
		return await app.send_edit(m, "No need to approve innocent bots !", mono=True, delme=3)
	await app.send_edit(m, "approving . . .", mono=True)
	reply = m.reply_to_message
	cmd = m.command

	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and app.long(m) == 1:
			return await app.send_edit(m, "Whom should i approve, piro ?", mono=True, delme=3)

		elif not reply and app.long(m) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				return await app.send_edit(m, "Please check username again . . .", delme=3, mono=True)

		else:
			return await app.send_edit(m, "Something went wrong . . .", mono=True, delme=2)

	info = await app.get_users(user_id)
	user_name = info.first_name
	try:
		app.set_whitelist(user_id, True)
		await app.send_edit(m, f"{info.mention} is now approved for pm.", delme=5)

		app.del_warn(user_id)

		if app.get_msgid(user_id):
			await old_msg(m, user_id)

	except Exception as e:
		await app.error(m, e)
		await app.send_edit(m, f"Something went wrong . . .", mono=True, delme=3)




@app.on_message(gen(["da", "disapprove"]))
async def diapprove_pm(_, m:Message):
	if m.chat.type == "bot":
		return await app.send_edit(m, "No need to approve innocent bots !", mono=True, delme=3)

	await app.send_edit(m, "disapproving . . .", mono=True)
	reply = m.reply_to_message
	cmd = m.command

	if m.chat.type == "private":
		user_id = m.chat.id
	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
		elif not reply and app.long(m) == 1:
			await app.send_edit(m, "Whom should i disapprove, piro ?", mono=True, delme=3)
		elif not reply and app.long(m) > 1:
			try:
				data = await app.get_users(cmd[1])
				user_id = data.id
			except (
				IndexError, 
				PeerIdInvalid, 
				UsernameNotOccupied, 
				UsernameInvalid
				):
				return await app.send_edit(m, "Please try again later . . .", delme=3)
		else:
			await app.send_edit(m, "Failed to disapprove user !", mono=True, delme=3)

	info = await app.get_users(user_id)
	user_name = info.first_name
	if user_name:
		app.del_whitelist(user_id)
		await app.send_edit(m, f"{info.mention} has been disapproved for pm!", delme=5)
		try:
			await app.send_message(
				app.LOG_CHAT, 
				f"#disallow\n\n{info.mention} has been disapproved for pm !"
			)
		except Exception as e:
			pass
	else:
		await app.send_edit(m, "Sorry there is no user id to disapprove . . .", mono=True, delme=3)


