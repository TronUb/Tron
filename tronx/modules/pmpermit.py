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
	""" Delete warn messages """
	if bool(app.get_msgid(user_id)) is True:
		old_msgs = app.get_msgid(user_id)
		await app.delete_messages(
			chat_id=m.chat.id, 
			message_ids=old_msgs
		)
		return True
	return False




async def send_warn(m: Message, user):
	""" Send warning messages """
	pic = app.PmpermitPic()
	text = app.PmpermitText()

	if pic:
		msg = await app.send_photo(
			m.chat.id,
			pic,
			caption=text
		)
		return True
	elif not pic:
		msg = await app.send_message(
			m.chat.id,
			text,
			disable_web_page_preview=True
			)
		return True
	else:
		return print("The bot didn't send pmpermit warning message.")
		return False
	app.set_msgid(user, msg.message_id)





# incoming autoblock
@app.on_message(filters.private & filters.incoming & (~filters.bot & ~filters.me), group=-1)
async def autoblock_handler(_, m: Message):
	try:
		users = []
		is_user = False
		pmlimit = app.PmpermitLimit()

		if bool(app.Pmpermit()) is False or m.chat.is_verified: # allow verified accounts
			return

		if bool(app.get_whitelist(m.chat.id)) is True:
			return
		else:
			# this will reduce the use of pyrogram's get_users method
			if bool(users):
				for x in users:
					if x.get(m.chat.id):
						is_user = True
						break

			if is_user:
				user = users.get(m.chat.id)
			else:
				user = await app.get_users(m.chat.id)
				users.append({m.chat.id : user}) # whole obj


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
						print(f"{user.first_name} was blocked in your pm for spamming.")
				else:
					await app.send_edit(m, f"Failed to block {user.first_name} because of spamming in pm", mono=True, delme=4)
			else:
				print("Something went wrong in pmpermit")
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["a", "approve"], allow = ["sudo"]), group=0)
async def approve_handler(_, m: Message):
	if m.chat.type == "bot":
		return await app.send_edit(m, "No need to approve innocent bots !", mono=True, delme=4)

	reply = m.reply_to_message
	cmd = m.command
	user_data = False

	if m.chat.type == "private":
		user_id = m.chat.id

	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id
	
		elif not reply and app.long(m) == 1:
			return await app.send_edit(m, "Whom should i approve, piro ?", mono=True, delme=4)

		elif not reply and app.long(m) > 1:
			try:
				user_data = await app.get_users(cmd[1])
				user_id = user_data.id
			except PeerIdInvalid:
				return await app.send_edit(m, "The username | user id is invalid.", mono=True, delme=4)
			except UsernameNotOccupied:
				return await app.send_edit(m, "No user like exists in telegram.", mono=True, delme=4)
			except UsernameInvalid:
				return await app.send_edit(m, "The username | user id is invalid.", mono=True, delme=4)

		else:
			return await app.send_edit(m, "Something went wrong.", mono=True, delme=4)
	if user_data:
		info = user_data
	else:
		info = await app.get_users(user_id)

	try:
		m = await app.send_edit(m, "`Approving` {info.mention} `. . .`")
		app.set_whitelist(user_id, True)
		await app.send_edit(m, f"{info.mention} `is now approved for pm.`", delme=4)
		app.del_warn(user_id)

		if app.get_msgid(user_id):
			await old_msg(m, user_id)

	except Exception as e:
		await app.send_edit(m, f"Something went wrong.", mono=True, delme=4)
		await app.error(m, e)




@app.on_message(gen(["da", "disapprove"], allow = ["sudo"]), group=-2)
async def diapprove_handler(_, m:Message):
	if m.chat.type == "bot":
		return await app.send_edit(m, "No need to approve innocent bots !", mono=True, delme=4)

	reply = m.reply_to_message
	cmd = m.command
	user_data = False

	if m.chat.type == "private":
		user_id = m.chat.id

	elif m.chat.type != "private":
		if reply:
			user_id = reply.from_user.id

		elif not reply and app.long(m) == 1:
			return await app.send_edit(m, "Whom should i disapprove, piro ?", mono=True, delme=4)

		elif not reply and app.long(m) > 1:
			try:
				user_data = await app.get_users(cmd[1])
				user_id = user_data.id
			except PeerIdInvalid:
				return await app.send_edit(m, "The username | user id is invalid.", mono=True, delme=4)
			except UsernameNotOccupied:
				return await app.send_edit(m, "This user doesn't exists in telegram.", mono=True, delme=4)
			except UsernameInvalid:
				return await app.send_edit(m, "The username | user id is invalid.", mono=True, delme=4)
		else:
			return await app.send_edit(m, "Failed to disapprove user !", mono=True, delme=4)
	if user_data:
		info = user_data
	else:
		info = await app.get_users(user_id)

	if info:
		m = await app.send_edit(m, f"`Disapproving` {info.mention} `. . .`")
		app.del_whitelist(user_id)
		await app.send_edit(m, f"{info.mention} `has been disapproved for pm.`", delme=4)
		try:
			await app.send_message(
				app.LOG_CHAT, 
				f"#disallow\n\n{info.mention} has been disapproved for pm !"
			)
		except PeerIdInvalid:
			print(f"{info.first_name} has been disapproved for pm")
	else:
		return await app.send_edit(m, "Sorry there is no user id to disapprove.", mono=True, delme=4)


