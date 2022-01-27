import time
import asyncio
import html

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, User

from pyrogram.errors import (
	UserAdminInvalid, 
	UsernameInvalid,
	UserNotParticipant,
	UsernameNotOccupied,
)
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters

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
		"kick" : "kick a user out of your group.",
		"unpin" : "unpin a pinned message in group",
		"unpin all" : "unpin all pinned messages in one command"
		}
		)
	}
)



def to_seconds(format, number): # number: int, format: s, m, h, d
	format_set = {"s": number, "m": number*60, "h": number*60*60, "d": number*60*60*24} 
	return int(format_set[format]) 




@app.on_message(gen("ban", allow_channel=True))
async def ban_hammer(_, m):
	try:
		# return if used in private
		await app.private(m)
		reply = m.reply_to_message
		user = False
		cmd = m.command
		ban_time = False

		if await app.IsAdmin(m) is True:
			await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
				if app.long(m) > 1:
					arg = cmd[1]
					ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
	
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to the user you want to ban . . .", mono=True)
				elif app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, cmd[1])
					if app.long(m) > 2:
						arg = cmd[2]
						ban_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			if user:
				if user.user.is_self:
					return await app.send_edit(m, "You can't ban yourself !", mono=True)
				elif user.status == "administrator":
					return await app.send_edit(m, "How am i supposed to ban an admin ?", mono=True)
				elif user.status == "creator":
					return await app.send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True)
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			if ban_time:
				await app.ban_chat_member(m.chat.id, user.user.id, time.time() + ban_time)
				await app.send_edit(m, f"Banned {user.user.mention} for {arg} ")
			else:
				await app.ban_chat_member(m.chat.id, user.user.id)
				await app.send_edit(m, f"Banned {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You are not an admin here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("banall", allow_channel=True))
async def ban_all(_, m):
	try: 
		await app.private(m)
		if await app.IsAdmin(m) is True:
			count = 0
			data = []
			data.clear()
			if app.long(m) == 1:
				return await app.send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2)
			elif app.long(m) > 1 and m.command[1] == "confirm":
				async for x in app.iter_chat_members(m.chat.id):
					if x.status == "member":
						await app.ban_chat_member(m.chat.id, x.user.id)
						count += 1
						await app.send_edit(m, f"Banned {x.user.mention} . . .")
				await app.send_edit(m, f"Banned {count} members !")
			elif app.long(m) > 1 and m.command[1] != "confirm":
				await app.send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2, mono=True)
		else:
			await app.send_edit(m, "`Sorry, you are not an admin here . . .`", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unban", allow_channel=True))
async def unban(_, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await app.send_edit(m, "You can't Unban yourself !", mono=True)
				elif user.status == "administrator":
					return await app.send_edit(m, "How am i supposed to ban an admin ?", mono=True)
				elif user.status == "creator":
					return await app.send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True)
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			await app.unban_chat_member(m.chat.id, user.user.id)
			await app.send_edit(m, f"Unbanned {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)
					



async def mute_user(m: Message, user_id, duration=0):
	return await app.restrict_chat_member(
		chat_id=m.chat.id,
		user_id=user_id,
		permissions=ChatPermissions(
			can_send_messages=False,
			can_send_media_messages=False,
			can_send_stickers=False,
			can_send_animations=False,
			can_send_games=True,
			can_use_inline_bots=False,
			can_add_web_page_previews=False,
			can_send_polls=False,
			can_change_info=False,
			can_invite_users=True,
			can_pin_messages=False
			),
		until_date=duration
		)





@app.on_message(gen("mute"))
async def mute_user(_, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		mute_time = False
		cmd = m.command

		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
				if app.long(m) > 1:
					arg = cmd[1]
					mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
					if app.long(m) > 2:
						arg = cmd[2]
						mute_time = to_seconds(arg[-1], int(arg.replace(arg[-1], "")))
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await app.send_edit(m, "You can't mute yourself !", mono=True)
				elif user.status == "administrator":
					return await app.send_edit(m, "How am i supposed to mute an admin ?", mono=True)
				elif user.status == "creator":
					return await app.send_edit(m, "How am i supposed to mute a creator of a group ?", mono=True)
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			if mute_time:
				await mute_user(m.chat.id, user.user.id, time.time()+mute_time)
				await app.send_edit(m, f"Muted {user.user.mention} for {arg}")
			else:
				await mute_user(m.chat.id, user.user.id)
				await app.send_edit(m, f"Muted {user.user.mention} in this chat for forever.")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unmute"))
async def unmute(_, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await app.send_edit(m, "You can't Unmute yourself !", mono=True)
				elif user.status == "administrator":
					return await app.send_edit(m, "How do i unmute an admin ?", mono=True)
				elif user.status == "creator":
					return await app.send_edit(m, "How do i unmute a creator ?", mono=True)
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			await app.restrict_chat_member(
				m.chat.id,
				user.user.id,
				permissions=ChatPermissions(
					can_send_messages=True,
					can_send_media_messages=True,
					can_send_stickers=True,
					can_send_animations=True,
					can_send_games=True,
					can_use_inline_bots=True,
					can_add_web_page_previews=True,
					can_send_polls=True,
					can_change_info=False,
					can_invite_users=True,
					can_pin_messages=False,
				)
				)
			await app.send_edit(m, f"Unmuted {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("kick", allow_channel=True))
async def kick_user(_, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

			if user:
				if user.user.is_self:
					return await app.send_edit(m, "You can't kick yourself !", mono=True)
				elif user.status == "administrator":
					return await app.send_edit(m, "How am i supposed to kick an admin ?", mono=True)
				elif user.status == "creator":
					return await app.send_edit(m, "How am i supposed to kick a creator of a group ?", mono=True)
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True)

			await app.kick(m.chat.id, user.user.id)
			await app.send_edit(m, f"Kicked {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("pin", allow_channel=True))
async def pin_message(_, m):
	reply = m.reply_to_message
	try:
		if m.chat.type in ["private", "bot"]:
			if not reply:
				return await app.send_edit("reply to some message, so that i can pin ", mono=True, delme=5)
			else:
				await reply.pin()
				return await app.send_edit(m, "Pinned message !", mono=True, delme=5)
		if await app.IsAdmin(m) is True:
			if reply:
				await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
				done = await reply.pin()
				await app.send_edit(m, "Pinned message!", mono=True) if done else await app.send_edit(m, "Failed to pin message", delme=2, mono=True)
			elif not reply:
				await app.send_edit(m, "Reply to a message so that I can pin that message . . .", delme=2, mono=True)    
		else:
			await app.send_edit(m, "Sorry, you don't have permissions to perform this action !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("unpin", allow_channel=True))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			await app.send_edit(m, "⏳ • Hold on . . .", mono=True)
			done = await reply.unpin()
			await app.send_edit(m, "Unpinned message !", mono=True) if done else await app.send_edit(m, "Failed to unpin message . . .", delme=2, mono=True)
		elif not reply and app.long(m) > 1:
			cmd = m.command[1]
			if cmd == "all":
				done = await app.unpin_all_chat_messages(m.chat.id)
				await app.send_edit(m, "Unpinned all pinned messages . . .", mono=True) if done else await app.send_edit(m, "Failed to unpin all messages . . .", delme=2, mono=True)
			elif cmd != "all":
				await app.send_edit(m, "Reply to a pinned message to unpin or use 'all' as suffix to unpin all pinned messages . . .", delme=2, mono=True)
			else:
				await app.send_edit(m, "Failed to unpin messages . . .", delme=2, mono=True)
		elif not reply and app.long(m) == 1:
			await app.send_edit(m, "Reply to the pinned message to unpin it !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("promote", allow_channel=True))
async def promote(_, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

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
				can_pin_messages=True, 
				can_invite_users=True,
				can_restrict_members=True,
				can_delete_messages=True,
				can_post_messages=True,
				)
			await app.send_edit(m, f"Promoted {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("demote", allow_channel=True))
async def demote(client, m):
	try:
		await app.private(m)
		reply = m.reply_to_message
		user = False
		if await app.IsAdmin(m) is True:
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.from_user.id)
			elif not reply:
				if app.long(m) == 1:
					return await app.send_edit(m, "Give me user id | username or reply to that user you want to unban . . .", mono=True, delme=4)
				if app.long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)

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
			await app.send_edit(m, f"Demoted {user.user.mention} in this chat !")
		else:
			return await app.send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)

	except (UsernameInvalid, UsernameNotOccupied):
		await app.send_edit(m, "The provided username | id is invalid !", mono=True, delme=5)
	except UserNotParticipant:
		await app.send_edit(m, "This user doesn't exist in this group !", mono=True, delme=5)
	except Exception as e:
		await app.error(m, e)
