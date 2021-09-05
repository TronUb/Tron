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
	Config
	)

from tronx.helpers import (
	gen,
	error,
	mymention,
	send_edit,
	# others 
	get_arg, 
	get_args, 
	GetUserMentionable, 
	mention_html, 
	mention_markdown, 
	CheckAdmin, 
	CheckReplyAdmin, 
	RestrictFailed,
	private,
	long,
)




CMD_HELP.update(
	{"utils" : (
		"utils",
		{
		"settitle [ @username ] [ title ]" : "Set title of an admin.",
		"invite [ @username ]" : "Invite a user in your chat.",
		"admins" : "Get list of admins.",
		"report [ reply to user ]" : "report a spammer or idiot.",
		"all" : "Tag recent 100 members, use carefully.",
		"bots" : "Get list of bots in a chat.",
		"kickme" : "leave a chat, use it carefully.",
		"members [ @username ]" : "Get number of members in  a chat.",
		"join [chat username or id]" : "Join a chat with just a command.",
		"slowmo [seconds]" : "Set slow mode in a chat, use 'off' as suffix to turn off slow mode . . .",
		}
		)
	}
)




@app.on_message(gen("settitle"))
async def admin_title(_, m: Message):
	if (m.chat.type == "private") and (len(m.command) == 1):
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if len(m.command) == 3:
		try:
			await send_edit(
				m, 
				"⏳ • hold on...")
				
			user_data = m.command[1]
			title = m.command[2]
			user = await app.get_users(user_data)
			admin = user.id
			user_name = user.first_name
			user_chat_info = await app.get_chat_member(m.chat.id, admin)
			is_admin = user_chat_info.status
			if "member" in is_admin:
				await send_edit(
					m, 
					f"{user_name} is not an admin in this chat ..."
					)
			else:
				await app.set_administrator_title(m.chat.id, admin, title)
				await send_edit(
					m, 
					f"**{user_name}'s** title is successfully changed to **{title}**")
		except Exception as e:
			await error(m, e)
	elif (len(m.command) == 2) and (m.reply_to_message):
		try:
			title = m.command[1]
			user = m.reply_to_message
			admin = user.id
			user_name = user.first_name
			user_chat_info = await app.get_chat_member(m.chat.id, admin)
			is_admin = user_chat_info.status
			if "member" in is_admin:
				await send_edit(
					m, 
					f"{user_name} is not an admin in this chat ..."
					)
			else:
				await app.set_administrator_title(m.chat.id, admin, title)
				await send_edit(
					m, 
					f"{user_name}'s title is successfully changed to `{title}`"
					)
		except Exception as e:
			await error(m, e)
	else:
		print("Something went wrong in .settitle command in admin plugin.")




@app.on_message(gen("invite"))
async def invite(_, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	await send_edit(
		m, 
		"⏳ • Hold on...")
		
	reply = m.reply_to_message
	if reply:
		user = reply.from_user["id"]
	else:
		user = get_arg(m)
		if not user:
			await send_edit(
				m, 
				"I can't invite ghost, can I ?"
				)
			return
	get_user = await app.get_users(user)
	try:
		await app.add_chat_members(
			m.chat.id, 
			get_user.id
			)
		await send_edit(
			m, 
			f"Added {get_user.first_name} to the chat!"
			)
	except USERNAME_NOT_OCCUPIED:
		await send_edit(
			m, 
			"The user / bot does not exist, please çheck again ..."
			)




@app.on_message(gen(["admins", "adminlist"]))
async def adminlist(client, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	await send_edit(
		m, 
		"⏳ • Hold on...")
		
	replyid = None
	toolong = False
	if len(m.text.split()) >= 2:
		chat = m.text.split(None, 1)[1]
		grup = await app.get_chat(chat)
	else:
		chat = m.chat.id
		grup = await app.get_chat(chat)
	if m.reply_to_message:
		replyid = m.reply_to_message.message_id
	alladmins = app.iter_chat_members(
		chat, 
		filter="administrators"
		)
	creator = []
	admin = []
	badmin = []
	async for a in alladmins:
		try:
			user_info = a.user.first_name + " " + a.user.last_name
		except:
			user_info = a.user.first_name
		if user_info == None:
			user_info = "💀 Deleted account"
		if a.status == "administrator":
			if a.user.is_bot == True:
				badmin.append(mention_markdown(a.user.id, user_info))
			else:
				admin.append(mention_markdown(a.user.id, user_info))
		elif a.status == "creator":
			creator.append(mention_markdown(a.user.id, user_info))
	admin.sort()
	badmin.sort()
	totaladmins = len(creator)+len(admin)+len(badmin)
	teks = "**Admins in `{}`\n\n".format(grup.title)
	teks += "**• CREATOR:** \n"
	for x in creator:
		teks += "{}\n\n".format(x)
		if len(teks) >= 4096:
			await m.reply(
				m.chat.id, 
				teks, 
				reply_to_message_id=replyid
				)
			teks = ""
			toolong = True
	teks += "\n**• {} USER ADMINS:**\n".format(len(admin))
	for x in admin:
		teks += "{}\n".format(x)
		if len(teks) >= 4096:
			await m.reply(
				m.chat.id, 
				teks, 
				reply_to_message_id=replyid
				)
			teks = ""
			toolong = True
	teks += "**• {} BOT ADMINS:**\n\n".format(len(badmin))
	for x in badmin:
		teks += " • {}\n".format(x)
		if len(teks) >= 4096:
			await m.reply(
				m.chat.id, 
				teks, 
				reply_to_message_id=replyid
				)
			teks = ""
			toolong = True
	teks += "\nTotal `{}` Admins".format(totaladmins)
	if toolong:
		await m.reply(
			m.chat.id, 
			teks, 
			reply_to_message_id=replyid
			)
	else:
		await send_edit(m, teks)




@app.on_message(gen("report"))
async def report_admin(_, m: Message):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	if len(m.text.split()) >= 2:
		text = m.text.split(None, 1)[1]
	else:
		text = None
	grup = await app.get_chat(m.chat.id)
	alladmins = app.iter_chat_members(
		m.chat.id, 
		filter="administrators"
		)
	admin = []
	async for a in alladmins:
		if a.status == "administrator" or a.status == "creator":
			if a.user.is_bot == False:
				admin.append(mention_html(a.user.id, "\u200b"))
	if m.reply_to_message:
		await send_edit(
			m, 
			"⏳ • Hold on...")
			
		if text != None:
			teks = '{} is reported to admins.\n**Reason:** {}'.format(mention_markdown(m.reply_to_message.from_user.id, m.reply_to_message.from_user.first_name), text)
		else:
			teks = '{} is reported to admins.'.format(mention_markdown(m.reply_to_message.from_user.id, m.reply_to_message.from_user.first_name))
	else:
		await send_edit(
			m, 
			"⏳ • Hold on...")
			
		if text:
			teks = '{}'.format(html.escape(text))
		else:
			teks = "Calling admins in {}...".format(grup.title)
	teks += "".join(admin)
	if m.reply_to_message:
		await app.send_message(
			m.chat.id, 
			f"{teks}",
			reply_to_message_id=m.reply_to_message.message_id, 
			parse_mode="html"
			)
	else:
		await app.send_message(
			m.chat.id, 
			teks, 
			parse_mode="html")




@app.on_message(gen(["all"]) & filters.regex("@all"))
async def tag_all_users(app, m: Message):
	if m.chat.type == "private":
		await send_edit(
			m,
			"Please use it in groups ..."
			)
		return
	await m.delete()
	if len(m.text.split()) >= 2:
		text = m.text.split(None, 1)[1]
	else:
		text = "Hello Everyone "
	await send_edit(
		m,
		"⏳ • Hold on..."
		)
		
	tip = app.iter_chat_members(m.chat.id)
	async for a in tip:
		if a.user.is_bot == False:
			text += mention_html(a.user.id, "\u200b")
	if m.reply_to_message:
		await app.send_message(
			m.chat.id, 
			text, 
			reply_to_message_id=m.reply_to_message.message_id, 
			parse_mode="html"
			)
	else:
		await app.send_message(
			m.chat.id, 
			text, 
			parse_mode="html"
			)




@app.on_message(gen(["bots"]))
async def get_list_bots(_, m: Message):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	replyid = None
	if len(m.text.split()) >= 2:
		chat = m.text.split(None, 1)[1]
		grp = await app.get_chat(chat)
	else:
		chat = m.chat.id
		grp = await app.get_chat(chat)
	if m.reply_to_message:
		replyid = m.reply_to_message.message_id
	await m.edit("⏳ • Hold on...")
	getbots = app.iter_chat_members(chat)
	bots = []
	async for a in getbots:
		try:
			bot_info = a.user.first_name + " " + a.user.last_name
		except:
			bot_info = a.user.first_name
		if bot_info == None:
			bot_info = "💀 Deleted account"
		if a.user.is_bot == True:
			bots.append(mention_markdown(a.user.id, bot_info))
	teks = "**Bots in `{}`**\n\n".format(grp.title)
	for x in bots:
		teks += " • {}\n".format(x)
	teks += "\nTotal {} Bots".format(len(bots))
	if replyid:
		await app.send_m(
			m.chat.id, 
			teks, 
			reply_to_message_id=replyid
			)
	else:
		await send_edit(m, teks)




@app.on_message(gen("kickme"))
async def leave(client, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use it in groups ..."
			)
		return
	try:
		m = await send_edit(
			m, 
			f"{mymention()} left the chat ..."
			)
		await asyncio.sleep(1)
		await app.leave_chat(
			chat_id=m.chat.id
			)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("members"))
async def get_member_count(client, m):
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Try this command in groups ..."
			)
		return
	if len(m.command) == 1:
		try:
			num = await app.get_chat_members_count(m.chat.id)
			await send_edit(
				m,
				f"{num} members"
				)
		except USERNAME_NOT_OCCUPIED:
			await send_edit(
				m,
				"The username does not exist ..."
				)
	elif len(m.command) <= 2:
		try:
			mid = m.command[1]
			num = await app.get_chat_members_count(mid)
			await send_edit(
				m,
				f"`{num}` members in {mid}"
				)
		except USERNAME_NOT_OCCUPIED:
			await send_edit(
				m, 
				"The username does not exist ..."
				)
	else:
		await send_edit(
			m, 
			f"Usage: `{PREFIX}members` or `{PREFIX}members <chat username>` "
			)




@app.on_message(gen("join"))
async def join_chats(_, m: Message):
	if long(m) == 1:
		await send_edit(m, "Give me some chat id / username after command . . .")
		return
	elif long(m) > 1:
		chat = m.command[1]
		try:
			data = await app.get_chat(chat)
			done = await app.join_chat(chat)
			if data and done:
				await send_edit(m, f"Successfully joined `{data.title}`")
			else:
				await send_edit(m, "Couldn't join chat !")
		except Exception as e:
			await error(m, e)
	elif long(m) > 4096:
		await send_edit(m, "Maximum 4096 characters . . .")




@app.on_message(gen("slowmo"))
async def slow_mode(_, m: Message):
	await private(m)
	if await CheckAdmin(m) is True:
		if long(m) == 1:
			sec = 5
		elif long(m) > 1:
			try:
				sec = m.command[1]
				if not sec.isdigit() and sec != "off":
					await send_edit(m, "Sir, please give me some seconds in numbers after command . . .")
					return
				if sec == "off":
					sec = None
					await app.set_slow_mode(m.chat.id, sec)
					await send_edit(m, "Slow mode is now turned off.")
				else:
					await app.set_slow_mode(m.chat.id, sec)
					await send_edit(m, f"Updated slow mode to {sec} seconds.")
			except Exception as e:
				await error(m, e)
		else:
			return
	else:
		await send_edit(m, "Sorry, you are not an admin here . . .")