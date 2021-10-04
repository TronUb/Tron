import os, time, math, asyncio

from functools import partial
from datetime import datetime

from pyrogram import filters, Client
from pyrogram.types import (
	Message, 
	User, 
	InlineKeyboardMarkup, 
	InlineKeyboardButton
	)
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid

from tronx import (
	app, 
	CMD_HELP, 
	log,
	Config,
	PREFIX
	)




from tronx.helpers import (
	gen,
	send_edit,
	error,
	long,
)




date_dict = []




CMD_HELP.update(
	{"profile" : (
		"profile",
		{
		"whois [reply to message]" : "get a small piece of information of a user.",
		"block [username] or [reply to user]" : "Block a user from sending message in your pm.",
		"unblock [username] or [reply to user]" : "Unblock a user and allow him to send messages in your pm.",
		"repo" : "Get Tron Userbot official repository link.",
		"rem [lname] or [username]" : "Remove last name or username from profile.",
		"set [fname] or [lname ] or [username] or [bio] and [text]" : "Choose a option from command and set anything in your profile.",
		"uinfo [reply to user]" : "Get Full Info Of A Specific User.\nThis Command Includes More Details.",
		"sc [reply to user]" : "Find Out Groups Of A Specific User, Reply To That User.",
		"sg [reply to user]" : "Get name & username history of a particular user in groups or private chats.",
		"men [username] [text]" : "Mention a user in a specific text.",
		}
		)
	}
)




men = partial("<a href='tg://user?id={}'>{}</a>".format)


infotext = (
	"**NAME:** `{full_name}`\n"
	"**USER ID:** `{user_id}`\n"
	"**Mention:** [{full_name}](tg://user?id={user_id})\n"
	"**USERNAME:** @{username}\n"
	"**DC ID:** {dc_id}\n"
)




def FullName(user: User):
	return user.first_name + " " + user.last_name if user.last_name else user.first_name




@app.on_message(gen("whois"))
async def whois(_, m: Message):
	reply = m.reply_to_message
	cmd = m.command
	await m.edit("...")

	if reply and long(m) == 1:
		get_user = reply.id
	elif not reply and long(m) == 1:
		get_user = m.from_user.id
	elif long(m) > 1:
		get_user = cmd[1]
	else:
		get_user = False

	try:
		if get_user:
			user = await app.get_users(get_user)
	except PeerIdInvalid:
		await m.reply("I don't know that User.")
		return

	pfp = await app.get_profile_photos(user.id)
	if not pfp:
		await send_edit(
			m.chat.id,
			infotext.format(
				full_name=FullName(user),
				user_id=user.id,
				first_name=user.first_name,
				username=user.username or "",
				dc_id=user.dc_id
			),
		disable_web_page_preview=True,
		)
	else:
		await app.send_cached_media(
			m.chat.id, 
			file_id = pfp[0].file_id,
			caption=infotext.format(
				full_name=FullName(user),
				user_id=user.id,
				first_name=user.first_name,
				username=user.username or "",
				dc_id=user.dc_id
			)
		)
		




@app.on_message(gen("id"))
async def id(_, m: Message):
	cmd = m.command
	chat_id = m.chat.id
	reply = m.reply_to_message

	if not reply and len(cmd) == 1:
		get_user = m.from_user.id
	elif reply and len(cmd) == 1:
		get_user = reply.from_user.id
	elif len(cmd) > 1:
		get_user = cmd[1]
		try:
			get_user = int(cmd[1])
		except ValueError:
			pass
	try:
		user = await app.get_users(get_user)
	except PeerIdInvalid:
		await m.edit("I don't know that User.")
		return
	text = "**User ID**: `{}`\n**Chat ID**: `{}`".format(user.id, chat_id)
	await m.edit(text)




@app.on_message(gen(["men", "mention"]))
async def mention(_, m: Message):
	if len(m.command) < 3:
		await m.edit("Incorrect input.\n\n**Example** : `.men @tronuserbot CTO`")
		await asyncio.sleep(2)
		await m.delete()
		return
	try:
		user = await app.get_users(m.command[1])
	except Exception:
		await m.edit("User not found !")
		await asyncio.sleep(2)
		await m.delete()
		return
	_men = men(user.id, " ".join(m.command[2:]))
	await m.edit(_men)




@app.on_message(gen("uinfo"))
async def get_full_user_info(_, m: Message):
	await m.edit('scrapping info...')
	reply = m.reply_to_message

	if reply:
		user = reply.from_user
	elif not reply:
		user = m.from_user

	pfp = await app.get_profile_photos(user.id)
	if pfp:
		p_id = pfp[0].file_id
	else:
		p_id = False

	try:
		duo = f"• ID: `{user.id}`\n"
		duo += f"• NAME: `{user.first_name}`\n"
		duo += f"• DC ID: `{user.dc_id}`\n"
		duo += f"• BOT: `{user.is_bot}`\n"
		duo += f"• FAKE: `{user.is_fake}`\n"
		duo += f"• SCAM: `{user.is_scam}`\n"
		duo += f"• NAME: `{user.first_name}`\n"
		duo += f"• STATUS: `{user.status}`\n"
		duo += f"• IS IT ME: `{user.is_self}`\n"
		duo += f"• DELETED: `{user.is_deleted}`\n"
		duo += f"• CONTACT: `{user.is_contact}`\n"
		duo += f"• VERIFIED: `{user.is_verified}`\n"
		duo += f"• RESTRICTED: `{user.is_restricted}`\n"

		if p_id:
			await app.send_cached_media(
				m.chat.id, 
				file_id=p_id, 
				caption=duo
			)
		elif p_id is False:
			await send_edit(m, duo)
	except Exception as e:
		await send_edit(m, "Try again later . . .")
		await error(m, e)




@app.on_message(gen(["sc", "scan"]))
async def tg_scanner(_, m: Message):
	if m.reply_to_message:
		await m.edit("Checking database . . .")
		await app.forward_messages(
			"@tgscanrobot", 
			m.chat.id, 
			m.reply_to_message.message_id
			)
		time.sleep(1)
		msg = await app.get_history(
			"@tgscanrobot", 
			limit=1
			)
		if msg:
			user = "⧓ " + msg[0].text.split("\n\n1. ")[0]
			await m.edit(user)
		else:
			await m.edit(
				"No information found !"
				)
	else:
		await m.edit("reply to someone's message...")
		time.sleep(3)
		await m.delete()




@app.on_message(gen("block"))
async def block_pm(_, m: Message):
	if len(m.command) >= 2:
		user = m.text.split(None, 1)[1]
		try:
			await app.unblock_user(user)
			await m.edit_text("`Blocked User`")
		except Exception as e:
			await error(m, e)
	elif m.reply_to_message:
		user = m.reply_to_message.from_user.id
		try:
			await app.unblock_user(user)
			await m.edit_text("`Blocked User`")
		except Exception as e:
			await error(m, e)




@app.on_message(gen("unblock"))
async def unblock_pm(_, m: Message):
	if len(m.command) >= 2:
		user = m.text.split(None, 1)[1]
		try:
			await app.unblock_user(user)
			await m.edit_text("`Unblocked User`")
		except Exception as e:
			await error(m, e)
	elif m.reply_to_message:
		user = m.reply_to_message.from_user.id
		try:
			await app.unblock_user(user)
			await m.edit_text("`Unblocked User`")
		except Exception as e:
			await error(m, e)
	return




@app.on_message(gen("sg"))
async def check_name_history(_, m: Message):
	if m.reply_to_message:
		await m.edit("Checking History...")
		await app.forward_messages(
			"@SangMataInfo_bot", 
			m.chat.id, 
			m.reply_to_message.message_id
			)
		is_no_record = False
		for x in range(8):
			time.sleep(1)
			msg = await app.get_history(
				"@SangMataInfo_bot", 
				limit=3
				)
			if msg[0].text == "No records found":
				await send_edit(m, "No records found")
				is_no_record = True
				await app.read_history("@SangMataInfo_bot")
				break
			if msg[0].from_user.id == 461843263 and msg[1].from_user.id == 461843263 and msg[2].from_user.id == 461843263:
				await app.read_history("@SangMataInfo_bot")
				break
			else:
				print("Failed, try again ({})".format(x+1))
				continue
		if is_no_record:
			return
		history_name = "1. " + msg[2].text.split("\n\n1. ")[1]
		username_history = "1. " + msg[1].text.split("\n\n1. ")[1]
		text = "**Name History for** [{}](tg://user?id={}) (`{}`)\n\n".format(m.reply_to_message.from_user.first_name, m.reply_to_message.from_user.id, m.reply_to_message.from_user.id) + history_name
		if long(m) <= 4096 and len(text) + len("\n\n**Username History**\n\n") + len(username_history) <= 4906:
			text += "\n\n**Username History**\n\n" + username_history
			await send_edit(m, text)
		else:
			await send_edit(m, text)
			await m.reply("\n\n**Username History**\n\n" + username_history)
		return
	else:
		await send_edit(m, "Reply to a user to get history of name / username.", delme=2)




@app.on_message(gen("set"))
async def update_profile(_, m: Message):
	custom = m.command
	text = m.text.split(None, 2)[2]

	if long(m) < 3:
		await m.edit("Please use text and suffix after command ...")
		return
	# set -> fname, lname & bio
	if long(m) > 2:
		if custom[1] in ["fname", "lname", "bio"]:
			await setprofile(
				m, 
				custom, 
				f"{text}"
			)
		elif custom[1] == "uname":
			app.update_username(
				f"{text}"
			)
	else:
		await m.edit(f"Please specify a correct suffix.", delme=2)
		return




@app.on_message(gen("rem"))
async def remove_profile(_, m: Message):
	if len(m.text) > 1:
		cmd = m.command[1]
	else:
		await send_edit(m,"what do you want to remove ?", delme=2)
		return
	try:
		if cmd in ["lname", "bio", "pfp", "uname"]:
			await rmprofile(m, cmd)
		else:
			await send_edit(m,"please use from the list:\n\n`lname`\n`bio`\n`pfp`\n`uname`", delme=2)
	except Exception as e:
		await error(m, e)




# set your profile stuffs 
async def setprofile(m: Message, args, kwargs):
	# set first name
	if args == "fname":
		try:
			await app.update_profile(
				first_name = f"{kwargs}"
				)
			await send_edit(
				m, 
				f"✅ Updated first name to [ {kwargs} ]"
				)
		except Exception as e:
			await error(m, e)
	# set last name
	elif args == "lname":
		try:
			await app.update_profile(
				last_name = f"{kwargs}"
			)
			await send_edit(
				m, 
				f"✅ Updated last name to [ {kwargs} ]"
				)
		except Exception as e:
			await error(m, e)
	# set bio
	elif args == "bio":
		try:
			await app.update_profile(
				bio = f"{kwargs}"
				)
			await send_edit(
				m, 
				f"✅ Updated bio to [ {kwargs}]"
				)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Please give correct format.", delme=2)
	return




# lost everything
async def rmprofile(m: Message, args):
	# delete last name
	if args == "lname":
		await app.update_profile(
			last_name = ""
			)
		await send_edit(
			m, 
			"✅ Removed last name from profile."
			)
	# delete bio
	elif args == "bio":
		await app.update_profile(
			bio = "")
		await send_edit(
			m, 
			"✅ Removed bio from profile."
			)
	# delete profile picture
	elif args == "pfp":
		photos = await app.get_profile_photos("me")
		if photos:
			await app.delete_profile_photos([p.file_id for p in photos[1:]])
			await send_edit(
				m, 
				"✅ Deleted all photos from profile."
				)
		else:
			await send_edit(m, "❌ There are no photos in your profile.")
	# delete username
	elif args == "uname":
		await app.update_username("")
		await send_edit(
			m, 
			"✅ Removed username from profile."
			)
	else:
		await m.edit("Give correct format.", delme=2)
	return




@app.on_message(filters.command("repo", PREFIX) & filters.me)
async def remove_pfp(_, m: Message):
	await send_edit(m, "[Here Is Tronuserbot Repo](https://github.com/beastzx18/Tron)")


