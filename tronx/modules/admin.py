import time
import asyncio
import html

from pyrogram.types import Message, ChatPermissions

from pyrogram.errors import (
	UserAdminInvalid, 
	UsernameInvalid,
	UserNotParticipant,
	UsernameNotOccupied,
)

from tronx import app

from tronx.helpers.filters import (
	gen,
)




app.CMD_HELP.update(
	{"admin" : (
		"admin", 
		{
		"ban [username | id | reply] [time]" : "bans a user, use it as timeban too",
		"banall [confirm]" : "Ban all members in by one command",
		"unban" : "unbans a user",
		"mute [username | id | reply] [time]" : "restricts a user from talking in groups",
		"unmute" : "unrestricts a user from talking in groups",
		"promote" : "promote a member to admin",
		"demote" : "demote a admin to a member",
		"pin" : "pin a message in group",
		"kick" : "kick a user out of your groups.",
		"unpin" : "unpin a pinned message.",
		"unpin all" : "unpin all pinned messages in one command"
		}
		)
	}
)



private = ("private", "bot")
def to_seconds(format, number): # number: int, format: s, m, h, d
	format_set = {"s": number, "m": number*60, "h": number*60*60, "d": number*60*60*24} 
	return int(format_set[format]) 




@app.on_message(gen("ban", allow = ["sudo", "channel"]))
async def ban_handler(_, m: Message):
	try:
		# return if used in private
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False
		cmd = m.command
		ban_time = False

		if app.long(m) == 1 and not reply:
			return await app.send_edit(m, "Reply or give some id | username after command.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin here or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			if app.long(m) > 1:
				arg = cmd[1]
				ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

		elif not reply:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, cmd[1])
				if app.long(m) > 2:
					arg = cmd[2]
					ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't ban yourself !", mono=True, delme=4)
			elif user.status == "administrator":
				return await app.send_edit(m, "How am i supposed to ban an admin ?", mono=True, delme=4)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True, delme=4)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		m = await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
		if ban_time:
			await app.ban_chat_member(m.chat.id, user.user.id, time.time() + ban_time)
			await app.send_edit(m, f"Banned {user.user.mention} for {arg}", delme=4)
		else:
			await app.ban_chat_member(m.chat.id, user.user.id)
			await app.send_edit(m, f"Banned {user.user.mention} in this chat.", delme=4)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("banall", allow = ["channel"]))
async def banall_handler(_, m: Message):
	try: 
		await app.private(m)
		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin or you don't have enough admin rights.", mono=True, delme=4)

		count = 0
		data = []
		data.clear()

		if app.long(m) == 1:
			return await app.send_edit(m, "Use '`confirm`' text after command to ban all members.", mono=True, delme=4)
		elif app.long(m) > 1 and m.command[1] == "confirm":
			async for x in app.iter_chat_members(m.chat.id):
				if x.status == "member":
					await app.ban_chat_member(m.chat.id, x.user.id)
					count += 1
					m = await app.send_edit(m, f"Banned {x.user.mention} . . .")
			await app.send_edit(m, f"Banned {count} members !")
		elif app.long(m) > 1 and m.command[1] != "confirm":
			await app.send_edit(m, "Use '`confirm`' text after command to ban all members.", mono=True, delme=4)

	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unban", allow = ["sudo", "channel"]))
async def unban_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False

		if not reply and app.long(m) == 1:
			return await app.send_edit(m, "Reply to a user or give me the username | id of that user.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
		elif not reply:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't unban yourself !", mono=True, delme=4)
			elif user.status == "administrator":
				return await app.send_edit(m, "How am i supposed to unban an admin ?", mono=True, delme=4)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to unban a creator of a group ?", mono=True, delme=4)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		m = await app.send_edit(m, "Unbanning . . .", mono=True)
		done = await app.unban_chat_member(m.chat.id, user.user.id)
		if done:
			await app.send_edit(m, f"Unbanned {user.user.mention} in this chat.", delme=4)
		else:
			await app.send_edit(m, "Failed to unabn this user.", mono=True, delme=4)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)
					



async def mute_user(chat_id, user_id, duration=0):
	return await app.restrict_chat_member(
		chat_id=chat_id,
		user_id=user_id,
		permissions=ChatPermissions(
			can_send_messages=False,
			can_send_media_messages=False,
			can_send_other_messages=False,
			can_add_web_page_previews=False,
			can_send_polls=False,
			can_change_info=False,
			can_invite_users=True,
			can_pin_messages=False
			),
			until_date=duration
		)





@app.on_message(gen("mute", allow = ["sudo"]))
async def mute_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False
		mute_time = False
		cmd = m.command

		if not reply and app.long(m) == 1:
			return await app.send_edit(m, "Reply to a user or give me username | id of that user.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			if app.long(m) > 1:
				arg = cmd[1]
				mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))

		elif not reply:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])
				if app.long(m) > 2:
					arg = cmd[2]
					mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't mute yourself !", mono=True, delme=4)
			elif user.status == "administrator":
				return await app.send_edit(m, "How am i supposed to mute an admin ?", mono=True, delme=4)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to mute a creator of a group ?", mono=True, delme=4)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		if mute_time:
			await mute_user(m.chat.id, user.user.id, int(time.time() + mute_time))
			await app.send_edit(m, f"Muted {user.user.mention} for {arg}")
		else:
			await mute_user(m.chat.id, user.user.id)
			await app.send_edit(m, f"Muted {user.user.mention} in this chat for forever.", delme=4)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unmute", allow = ["sudo"]))
async def unmute_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False

		if not reply and app.long(m) == 1:
			return await app.send_edit(m, "Reply to a user or give me the username | id of that user.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
		elif not reply:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't unmute yourself !", mono=True, delme=4)
			elif user.status == "administrator":
				return await app.send_edit(m, "How do i unmute an admin ?", mono=True, delme=4)
			elif user.status == "creator":
				return await app.send_edit(m, "How do i unmute a creator ?", mono=True, delme=4)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

		await app.restrict_chat_member(
			m.chat.id,
			user.user.id,
			permissions=ChatPermissions(
				can_send_messages=True,
				can_send_media_messages=True,
				can_send_other_messages=True,
				can_add_web_page_previews=True,
				can_send_polls=True,
				can_change_info=False,
				can_invite_users=True,
				can_pin_messages=False
			)
		)
		await app.send_edit(m, f"Unmuted {user.user.mention} in this chat.", delme=4)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("kick", allow = ["sudo", "channel"]))
async def kick_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False

		if not reply and app.long(m) == 1:
			return await app.send_edit(m, "Reply to a user or give me username | id of that user.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not admin or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
		else:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't kick yourself !", mono=True)
			elif user.status == "administrator":
				return await app.send_edit(m, "How am i supposed to kick an admin ?", mono=True)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to kick a creator of a group ?", mono=True)
		else:
			return await app.send_edit(m, "Something went wrong.", mono=True, delme=4)

		m = await app.send_edit(m, "Kicking . . .", mono=True)
		done = await app.kick_user(m.chat.id, user.user.id)
		if done:
			await app.send_edit(m, f"Kicked {user.user.mention} in this chat.", delme=4)
		else:
			await app.send_edit(m, "Failed to kick to user.", mono=True, delme=4)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("pin", allow = ["sudo", "channel"]))
async def pin_handler(_, m: Message):
	try:
		arg = True
		cmd = m.command
		reply = m.reply_to_message

		if app.long(m) > 1:
				arg = False if cmd[1] == "loud" else True

		if m.chat.type in private:
			if not reply:
				return await app.send_edit(m, "Reply to some message, so that i can pin that message.", mono=True, delme=4)

			done = await reply.pin(disable_notification=arg)
			if done:
				return await app.send_edit(m, "Pinned message !", mono=True, delme=4)
			else:
				return await app.send_edit(m, "Failed to pin message.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin here or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			m = await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
			done = await reply.pin(disable_notification=arg)
			if done:
				await app.send_edit(m, "Pinned message.", mono=True, delme=4)
			else:
				await app.send_edit(m, "Failed to pin message.", mono=True, delme=4)
		else:
			await app.send_edit(m, "Reply to a message so that I can pin that message.", mono=True, delme=4)    

	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unpin", allow = ["sudo", "channel"]))
async def unpin_handler(_, m: Message):
	try:
		cmd = m.command
		reply = m.reply_to_message

		if not reply and app.long(m) == 1:
			return await app.send_edit(m, "Reply to a message or use `all` as a prefix to unpin all pinned message.", mono=True, delme=4)

		if reply:
			m = await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
			done = await reply.unpin()
			if done:
				await app.send_edit(m, "Unpinned message.", mono=True) 
			else:
				await app.send_edit(m, "Failed to unpin message.", mono=True, delme=4)
		elif not reply and app.long(m) > 1:
			if cmd[1] == "all":
				done = await app.unpin_all_chat_messages(m.chat.id)
				if done:
					await app.send_edit(m, "Unpinned all pinned messages . . .", mono=True) 
				else:
					await app.send_edit(m, "Failed to unpin all messages.", mono=True, delme=4)
			elif cmd[1] != "all":
				await app.send_edit(m, "Reply to a pinned message to unpin or use `all` as a suffix to unpin all pinned messages.", mono=True, delme=4)
			else:
				await app.send_edit(m, "Failed to unpin all messages.", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("promote", allow = ["sudo", "channel"]))
async def promote_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False

		if app.long(m) == 1 and not reply:
			return await app.send_edit(m, "Reply to user or give me username | id of that user.", mono=True, delme=4)

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not admin or you don't have enough admin rights.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
		else:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't promote yourself !", mono=True)
			elif user.status == "administrator":
				return await app.send_edit(m, "How am i supposed to promote already promoted user ?", mono=True)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to promote a creator of a group ? wth ?", mono=True)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True)

		await app.promote_chat_member(
			m.chat.id, 
			user.user.id,
			is_anonymous=False,
			can_change_info=True,
			can_manage_voice_chats=True,
			can_manage_chat=True,
			can_delete_messages=True,
			can_edit_messages=True,
			can_invite_users=True,
			can_promote_members=False,
			can_restrict_members=True,
			can_pin_messages=True,
			can_post_messages=True,
		)
		m = app.send_edit(m, "Promoting . . .", mono=True)
		await app.send_edit(m, f"Promoted {user.user.mention} in this chat !")

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("demote", allow = ["sudo", "channel"]))
async def demote_handler(_, m: Message):
	try:
		if m.chat.type in private:
			return await app.private(m)

		reply = m.reply_to_message
		user = False

		if await app.IsAdmin(m) is False:
			return await app.send_edit(m, "You're not an admin here or you don't have enough rights.", mono=True, delme=4)

		if app.long(m) == 1 and not reply:
			return await app.send_edit(m, "Reply to user or give me username | id of that user.", mono=True, delme=4)

		if reply:
			user = await app.get_chat_member(m.chat.id, reply.from_user.id)
		else:
			if app.long(m) > 1:
				user = await app.get_chat_member(m.chat.id, m.command[1])

		if user:
			if user.user.is_self:
				return await app.send_edit(m, "You can't demote yourself !", mono=True)
			elif user.status == "creator":
				return await app.send_edit(m, "How am i supposed to demote a creator of a group ?", mono=True)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True)

		await app.promote_chat_member(
				m.chat.id,
				user.user.id,
				is_anonymous=False,
				can_change_info=False,
				can_manage_voice_chats=False,
				can_manage_chat=False,
				can_delete_messages=False,
				can_edit_messages=False,
				can_invite_users=False,
				can_promote_members=False,
				can_restrict_members=False,
				can_pin_messages=False,
				can_post_messages=False,
		)
		m = await app.send_edit(m, "Demoting . . .", mono=True)
		await app.send_edit(m, f"Demoted {user.user.mention} in this chat !")

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=4)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)
