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

from tronx.helpers import (
	get_arg, 
	get_args, 
	GetUserMentionable, 
	mention_html, 
	mention_markdown, 
	CheckAdmin, 
	CheckReplyAdmin, 
	RestrictFailed,
	gen,
	error, 
	send_edit,
	private,
	code,
	long,
	kick,
)




CMD_HELP.update(
	{"admin" : (
		"admin", 
		{
		"ban" : "bans a user",
		"banall [confirm]" : "Ban all members in by one command",
		"unban" : "unbans a user",
		"mute" : "restricts a user from talking in groups",
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




@app.on_message(gen("ban"))
async def ban_hammer(_, m):
	try:
		# return if used in private
		await private(m)
		reply = m.reply_to_message
		user = False
		if await CheckAdmin(m) is True:
			await send_edit(m, "⏳ • Hold on . . .", mono=True)
			if reply:
				user = await app.get_chat_member(m.chat.id, reply.user.id)
			elif not reply:
				if long(m) == 1:
					return await send_edit(m, "Give me user id | username or reply to the user you want to ban . . .")
				elif long(m) > 1:
					user = await app.get_chat_member(m.chat.id, m.command[1])
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			if user:
				if user.user.is_self:
					return await send_edit(m, "You can't ban yourself !", mono=True)
				elif user.status == "administrator":
					return await send_edit(m, "How am i supposed to ban an admin ?", mono=True)
				elif user.status == "creator":
					return await send_edit(m, "How am i supposed to ban a creator of a group ?", mono=True)
			else:
				return await send_edit(m, "Something went wrong !", mono=True)

			await kick(m.chat.id, user.user.id)
			await send_edit(m, f"Banned {user.user.mention} in this chat !")
	except Exception as e:
		await error(m, e)




@app.on_message(gen("banall"))
async def ban_all(_, m):
	await private(m)
	if await CheckAdmin(m) is True:
		try:
			count = 0
			data = []
			data.clear()
			if long(m) == 1:
				await send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2)
			elif long(m) > 1 and m.command[1] == "confirm":
				data = await app.get_chat_members(m.chat.id)
				for x in data:
					if x.status == "member":
						await kick(m.chat.id, x.user.id)
						count += 1
						await send_edit(m, f"Banned {x.user.first_name}", mono=True)
				await send_edit(m, f"Banned {count} members !")
			elif long(m) > 1 and m.command[1] != "confirm":
				await send_edit(m, "Use '`confirm`' text after command to ban all members . . .", delme=2, mono=True)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "`Sorry, you are not an admin here . . .`", delme=2, mono=True)




@app.on_message(gen("unban"))
async def unban(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:

		if reply:
			user = reply.from_user
			if user.is_self:
				await send_edit(m, "You are not banned in this group !", delme=2, mono=True)
				return
			await send_edit(m, "⏳ • Hold on...")
			done = await app.unban_chat_member(
				chat_id=m.chat.id,
				user_id=user.id
				)
			if done:
				await send_edit(m, f"Unbanned {mention_markdown(user.id, user.first_name)} in the current chat.") 
			elif not done:
				await send_edit(m, "I'm not able to unban this user . . .", delme=2, mono=True)
				return

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .", delme=2, mono=True)
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				if user.is_self:
					await send_edit(m, "You are not banned in this group !", delme=2, mono=True)
					return
				done = await app.unban_chat_member(
					chat_id=m.chat.id, 
					user_id=user.id
					)
				if done:
					await send_edit(m, f"Unbanned {mention_markdown(user.id, user.first_name)} in the current chat.")
				else:
					await send_edit(m, "I'm not able to unban this user . . .", delme=2, mono=True)

	else:
		await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)




@app.on_message(gen("mute"))
async def mute_user(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			user = reply.from_user
			if user.is_self:
				await send_edit(m, "You can't mute yourself !", delme=2, mono=True)
				return
			done = await app.restrict_chat_member(
				m.chat.id,
				user.id,
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
					can_pin_messages=False,
				)
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} has been muted")
			else:
				await send_edit(m, "Sorry, I am unable to mite this user . . .", delme=2, mono=True)

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .", delme=2, mono=True)

			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				if user.is_self:
					await send_edit(m, "You can't mute yourself !", delme=2, mono=True)
					return
				done = await app.restrict_chat_member(
					m.chat.id,
					user.id,
					permissions=mute_permission,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} has been muted.")
				else:
					await send_edit(m, "Sorry, I can't mute this user . . .", delme=2, mono=True)
			else:
				await send_edit(m, "Please try again later . . ." , delme=2, mono=True)

	else:
		await send_edit(m, "Sorry, You Are Not An Admin Here !", delme=1, mono=True)




@app.on_message(gen("unmute"))
async def unmute(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			user = reply.from_user
			if user.is_self:
				await send_edit(m, "You are not muted in this chat  !", delme=2, mono=True)
				return
			await send_edit(m, "⏳ • Hold on...", mono=True)
			done = await app.restrict_chat_member(
				m.chat.id,
				user.id,
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
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was unmuted !")
			else:
				await send_edit(m, "I can't unmute this user . . .", delme=2, mono=True)

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .", delme=2, mono=True)
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				if user.is_self:
					await send_edit(m, "You are not muted in this chat !", delme=2, mono=True)
					return
				done = await app.restrict_chat_member(
					chat_id=m.chat.id,
					user_id=user.id,
					permissions=unmute_permissions,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was unmuted.")
				else:
					await send_edit(m, "I can't unmute this user . . .", delme=2, mono=True)
			else:
				await send_edit(m, "Please try again later . . .", delme=2, mono=True)
	else:
		await send(m, "Sorry, Your Are Not An Admin Here ! ", delme=2, mono=True)




@app.on_message(gen("kick"))
async def kick_user(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			user = reply.from_user
			if user.is_self:
				await send_edit(m, "How can you kick yourself, masterrr !", delme=2, mono=True)
				return
			await send_edit(m, "⏳ • Hold on . . .", mono=True)
			done = await kick(m.chat.id, user.id)
			if done:
				await send_edit(m, f"Kicked {mention_markdown(user.id, user.first_name)} from the chat.")
			else:
				await send_edit(m, "I can't kick this user . . .", delme=2, mono=True)

		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Give me some id or username . . .", delme=2, mono=True)
			elif long(m) > 1:
				await send_edit(m, "⏳ • Hold on...")
				user = await app.get_users(m.command[1])
				if user.is_self:
					await send_edit(m, "How can you kick yourself, masterrr !", delme=2, mono=True)
					return
				done = await kick(m.chat.id, user.id)
				if done:
					await send_edit(m, f"Kicked {mention_markdown(user.id, user.first_name)} from this chat.")
				else:
					await send_edit(m, "I can't kick this user.", delme=2, mono=True)
			else:
				await send_edit(m, "Please try again later . . .", delme=2, mono=True)

	else:
		await send_edit(m, "Sorry, Your Are Not An Admin Here !", delme=2, mono=True)




@app.on_message(gen("pin"))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			await send_edit(m, "⏳ • Hold on...", mono=True)
			done = await reply.pin()
			if done:
				await send_edit(m, "Pinned message!", mono=True)
			else:
				await send_edit(m, "Failed to pin message", delme=2, mono=True)
		elif not reply:
			await send_edit(m, "Reply to a message so that I can pin that message . . .", delme=2, mono=True)     
	except Exception as e:
		await error(m, e)




@app.on_message(gen("unpin"))
async def pin_message(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			await send_edit(m, "⏳ • Hold on...", mono=True)
			done = reply.unpin()
			if done:
				await send_edit(m, "Unpinned message !", mono=True)
			else:
				await send_edit(m, "Failed to unpin message . . .", delme=2, mono=True)
		elif not reply and long(m) > 1:
			cmd = m.command[1]
			if cmd == "all":
				done = await app.unpin_all_chat_messages(m.chat.id)
				if done:
					await send_edit(m, "Unpinned all pinned messages . . .", mono=True)
				else:
					await send_edit(m, "Failed to unpin all messages . . .", delme=2, mono=True)
			elif cmd != "all":
				await send_edit(m, "Reply to a pinned message to unpin or use 'all' after unpin command to unpin all pinned message . . .", delme=2, mono=True)
			else:
				await send_edit(m, "Failed to unpin messages . . .", delme=2, mono=True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("promote"))
async def promote(_, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			if long(m) > 1:
				title = m.command[1]
				await app.set_administrator_title(m.chat.id, user.id, title)
			else:
				pass
			await send_edit(m, "⏳ • Hold on...", mono=True)
			user = reply.from_user
			if user.is_self:
					await send_edit(m, "You are already a admin !", delme=2, mono=True)
					return
			done = await app.promote_chat_member(
				m.chat.id, 
				user.id,
				can_pin_messages=True, 
				can_invite_users=True,
				)
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was promoted to admin !")
			else:
				await send_edit(m, "Failed to promote the user . . .", delme=2, mono=True)
		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or username . . .", delme=2, mono=True)
			elif long(m) > 1:
				user = await app.get_users(m.command[1])
				if user.is_self:
					await send_edit(m, "You are already a admin !", delme=2, mono=True)
					return
				await send_edit(m, "⏳ • Hold on...", mono=True)
				if long(m) > 2:
					title = m.command[2]
					await app.set_administrator_title(m.chat.id, user.id, title)
				else:
					pass
				done = await app.promote_chat_member(
					m.chat.id, 
					user.id,
					can_pin_messages=True, 
					can_invite_users=True,
					)
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} was promoted to admin !")
				else:
					await send_edit(m, "Failed to promote the user . . .", delme=2, mono=True)
			else:
				await send_edit(m, "Failed to promote user . . .", delme=2, mono=True)
	else:
		await send_edit(m, "Sorry, you are not an admin here . . .", delme=2, mono=True)




@app.on_message(gen("demote"))
async def demote(client, m):
	await private(m)
	reply = m.reply_to_message
	if await CheckAdmin(m) is True:
		if reply:
			await send_edit(m, "⏳ • Hold on...")
			user = reply.from_user
			if user.is_self:
				await send_edit(m, "You can't demote yourself !", delme=2, mono=True)
				return
			done = await app.promote_chat_member(
				m.chat.id,
				user.id,
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
			if done:
				await send_edit(m, f"{mention_markdown(user.id, user.first_name)} now removed from admin status !")
			else:
				await send_edit(m, "Failed to promote the user . . .", delme=2)
		elif not reply:
			if long(m) == 1:
				await send_edit(m, "Please give me some id or reply to that admin . . .", delme=2, mono=Trud)
			elif long(m) > 1:
				user = await app.get_user(m.command[1])
				if user.is_self:
					await send_edit(m, "You can't demote yourself !", delme=2, mono=True)
					return
				done = await app.promote_chat_member(
					m.chat.id,
					user.id,
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
				if done:
					await send_edit(m, f"{mention_markdown(user.id, user.first_name)} is now removed from admin status !")
			else: 
				await send_edit(m, "Please try again later . . .", delme=2)


