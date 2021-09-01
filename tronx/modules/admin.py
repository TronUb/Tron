import time
import asyncio
import html

from pyrogram import Client, filters
from pyrogram.types import Message, ChatPermissions, User

from pyrogram.errors import UserAdminInvalid
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters

from tronx import (
	app, 
	CMD_HELP, 
	PREFIX,
	Config,
	)
from tronx.helpers.utils import (
	get_arg, 
	get_args, 
	GetUserMentionable, 
	mention_html, 
	mention_markdown, 
	CheckAdmin, 
	CheckReplyAdmin, 
	RestrictFailed,
	)

from tronx.helpers import ( 
	gen,
	error, 
	send_edit,
	private,
	code,
)




CMD_HELP.update(
	{"admin" : (
		"admin", 
		{
		"ban" : "bans a user",
		"unban" : "unbans a user",
		"mute" : "restricts a user from talking in groups",
		"unmute" : "unrestricts a user from talking in groups",
		"promote" : "promote a member to admin",
		"demote" : "demote a admin to a member",
		"pin" : "pin a message in group",
		"unpin" : "unpin a pinned message in group",
		"unpin all" : "unpin all pinned messages in one command"
		}
		)
	}
)



@app.on_message(gen("ban"))
async def ban_hammer(_, m):
	# return if used in private
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
			# replies without suffix
		if reply and (len(m.command) == 1 or len(m.command) > 1):
			user = reply.from_user
			await send_edit(
				m, 
				"⏳ • Hold on..."
				)
			await app.kick_chat_member(
				m.chat.id,
				user.id
				)
			await send_edit(
				m, 
				f"Banned {user.first_name} in this chat ..."
				)
			# not replies 
		elif not reply:
			if len(m.command) == 1:
				await send_edit(
					m, 
					"Give me user id or username of that member you want to ban ..."
					)
				return
			elif len(m.command) > 1:
				user = m.command[1]
				user = await app.get_users(user)
				await send_edit(
					m, 
					"⏳ • Hold on..."
				)
				done = await app.kick_chat_member(
					chat_id=m.chat.id,
					user_id=get_user.id,
					)
				if done:
					await send_edit(
						m, 
						f"Banned {get_user.first_name} from the chat !"
						)
			elif len(m.command) > 4096:
				await send_edit(
					m, 
					"Minimum message length 4096 characters ..."
					)
		# reason not found
		else:
			await send_edit(
				m, 
				"I can't ban this user . . ."
		)
	else:
		await send_edit(
			m, 
			"Sorry, Your Are Not An Admin Here !"
			)




@app.on_message(gen("unban"))
async def unban(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply and (len(m.command) == 1 or len(m.command) > 1):
			user = reply.from_user
			if not user:
				await send_edit(
					m, 
					"I can't unban ghosts, can i ?"
					)
				return
			else:
				await send_edit(
					m, 
					"⏳ • Hold on..."
					)
				done = await app.unban_chat_member(
					chat_id=m.chat.id,
					user_id=user.id
					)
				if done:
					await send_edit(
						m, 
						f"Unbanned {user.first_name} in the current chat."
						)
				elif not done:
					await send_edit(
						m, 
						"I'm not able to unban this member ..."
						)
					return
		elif not reply:
			if len(m.command) > 1:
				user = m.command[1]
				await send_edit(
					m, 
					"⏳ • Hold on..."
					)
				get_user = await app.get_users(user)
				await app.unban_chat_member(
					chat_id=m.chat.id, 
					user_id=get_user.id
					)
				await send_edit(
					m, 
					f"Unbanned {get_user.first_name} from the chat."
					)
			elif len(m.command) == 1:
				await send_edit(
					m,
					"Please provide a user id or username to unban ..."
					)
				return
	else:
		await send_edit(
			m, 
			"Sorry, You Are Not An Admin Here !"
			)




# Mute Permissions
mute_permission = ChatPermissions(
	can_send_messages=False,
	can_send_media_messages=False,
	can_send_stickers=False,
	can_send_animations=False,
	can_send_games=False,
	can_use_inline_bots=False,
	can_add_web_page_previews=False,
	can_send_polls=False,
	can_change_info=False,
	can_invite_users=True,
	can_pin_messages=False,
)




@app.on_message(gen("mute"))
async def mute_hammer(_, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if await CheckAdmin(m) is True:
		if (m.reply_to_message) and (len(m.command) == 1):
			reply = m.reply_to_message
			if reply:
				user = reply.from_user["id"]
			else:
				user = get_arg(m)
				if not user:
					await send_edit(
						m, 
						"I Can't Mute A Ghost !!"
						)
					return
		elif not (m.reply_to_message) and (len(m.command) > 1):
			user = m.command[1]
		try:
			await send_edit(
				m, 
				"⏳ • Hold on...")
				
			get_user = await app.get_users(user)
			await app.restrict_chat_member(
				chat_id=m.chat.id,
				user_id=get_user.id,
				permissions=mute_permission,
			)
			await send_edit(
				m, 
				f"{get_user.first_name} has been muted."
				)
		except:
			await send_edit(
				m, 
				"I can't mute this user."
				)
	else:
		await send_edit(
			m, 
			"Sorry, You Are Not An Admin Here !"
			)




# Unmute permissions
unmute_permissions = ChatPermissions(
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




@app.on_message(gen("unmute"))
async def unmute(_, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if await CheckAdmin(m) is True:
		if (m.reply_to_message) and (len(m.command) == 1):
			reply = m.reply_to_message
			if reply:
				user = reply.from_user["id"]
			else:
				user = get_arg(m)
				if not user:
					await send_edit(
						m, 
						"Whom should I unmute ?"
						)
					return
		elif not (m.reply_to_message) and (len(m.command) > 1):
			user = m.command[1]
		try:
			await send_edit(
				m, 
				"⏳ • Hold on..."
				)
			get_user = await app.get_users(user)
			await app.restrict_chat_member(
			chat_id=m.chat.id,
			user_id=get_user.id,
			permissions=unmute_permissions,
			)
			await send_edit(
				m, 
				f"{get_user.first_name} was unmuted."
				)
		except:
			await send_edit(
				m, 
				"I can't unmute this user."
				)
	else:
		await send(
			m, 
			"Sorry, Your Are Not An Admin Here ! "
			)




@app.on_message(gen("kick"))
async def kick_user(_, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if await CheckAdmin(m) is True:
		reply = m.reply_to_message
		if reply:
			user = reply.from_user["id"]
		else:
			user = get_arg(m)
			if not user:
				await send_edit(
					m, 
					"Whom should I kick ?"
					)
				return
		try:
			await send_edit(
				m, 
				"⏳ • Hold on...")
				
			get_user = await app.get_users(user)
			await app.kick_chat_member(
				chat_id=m.chat.id,
				user_id=get_user.id,
				)
			await send_edit(
				m, 
				f"Kicked {get_user.first_name} from the chat."
				)
		except:
			await send_edit(
				m, 
				"I can't kick this user."
				)
	else:
		await send_edit(
			m, 
			"Sorry, Your Are Not An Admin Here !"
			)




@app.on_message(gen("pin"))
async def pin_message(_, m):
	if m.reply_to_message:
		try:
			await send_edit(
				m, 
				"⏳ • Hold on..."
				)
			await app.pin_chat_message(
				m.chat.id,
				m.reply_to_message.message_id,
				)
			await send_edit(
				m, 
				"`Pinned message!`"
				)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			"`Reply to a message so that I can pin that thing...`"
			)     
		await asyncio.sleep(1)
		await m.delete()




@app.on_message(gen("unpin"))
async def pin_message(_, m):
	replied = m.reply_to_message
	if replied:
		try:
			await send_edit(
				m, 
				"⏳ • Hold on..."
				)
			await app.unpin_chat_message(
				m.chat.id,
				m.reply_to_message.message_id
				)
			await send_edit(
				m, 
				"`Unpinned message!`"
				)
		except Exception as e:
			await error(m, e)
	elif not replied and len(m.text.split()) > 1:
		cmd = m.command[1]
		if cmd == "all":
			try:
				await app.unpin_all_chat_messages(m.chat.id)
			except Exception as e:
				await error(m, e)
		else:
			await send_edit(
				m, 
				"Use it properly, check help menu ..."
				)
	elif not replied and len(m.text.split()) == 1:
		await send_edit(
			m, 
			"Reply to a pinned message to unpin or use 'all' after unpin command to unpin all pinned message ..."
			)
	else:
		await send_edit(
			m, 
			"Something went wrong, please try again later ..."
			)




@app.on_message(gen("promote"))
async def promote(_, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if await CheckAdmin(m) is False:
		await send_edit(
			m, 
			"Sorry, You Are Not An Admin Here !"
			)
		return
	await send_edit(
		m, 
		"⏳ • Hold on..."
		)
	title = ""
	reply = m.reply_to_message
	if reply:
		user = reply.from_user["id"]
		title = str(get_arg(m))
	else:
		args = get_args(m)
		if not args:
			await send_edit(
				m, 
				"Am I Supposed To Promote A Ghost ?!"
				)
			return
		user = args[0]
		if len(args) > 1:
			title = " ".join(args[1:])
	get_user = await app.get_users(user)
	try:
		await app.promote_chat_member(
			m.chat.id, user, 
			can_pin_messages=True, 
			can_invite_users=True,
			)
		await send_edit(
			m, 
			f"{get_user.first_name} is now powered with admin rights with `{title}` as title!"
		)
	except Exception as e:
		await error(m, e)
	if title:
		try:
			await app.set_administrator_title(m.chat.id, user, title)
		except:
			pass




@app.on_message(gen("demote"))
async def demote(client, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if await CheckAdmin(m) is False:
		await send_edit(
			m, 
			"Sorry, Your Are Not An Admin Here !"
			)
		return
	await send_edit(
		m, 
		"⏳ • Hold on..."
		)
	reply = m.reply_to_message
	if reply:
		user = reply.from_user["id"]
	else:
		user = get_arg(m)
		if not user:
			await send_edit(
				"Tag A Person's Message to Demote !"
				)
			return
	get_user = await app.get_users(user)
	try:
		await app.promote_chat_member(
			m.chat.id,
			user,
			is_anonymous=False,
			can_change_info=False,
			can_delete_messages=False,
			can_edit_messages=False,
			can_invite_users=False,
			can_promote_members=False,
			can_restrict_members=False,
			can_pin_messages=False,
			can_post_messages=False,
			)
		await send_edit(
			m, 
			f"{get_user.first_name} is now stripped from their admin status !"
		)
	except Exception as e:
		await error(m, e)


