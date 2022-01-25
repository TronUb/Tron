import os
import time
import math
import asyncio

from functools import partial
from datetime import datetime

from pyrogram.types import (
	Message, 
	User, 
	InlineKeyboardMarkup, 
	InlineKeyboardButton
	)

from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid

from tronx import app

from tronx.helpers import (
	gen,
)




date_dict = []




app.CMD_HELP.update(
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


infotext = """
**NAME:** `{}`
**USER ID:** `{}`
**Mention:** [{}](tg://user?id={})
**USERNAME:** {}
**DC ID:** `{}`
"""




def FullName(user: User):
	return user.first_name + " " + user.last_name if user.last_name else user.first_name




@app.on_message(gen("whois"))
async def whois(_, m: Message):
	reply = m.reply_to_message
	cmd = m.command
	msg = await app.send_edit(m, "Processing . . .", mono=True)

	if reply and app.long(m) == 1:
		get_user = reply.id
	elif not reply and app.long(m) == 1:
		get_user = m.from_user.id
	elif app.long(m) > 1:
		get_user = cmd[1]
	else:
		get_user = False

	try:
		if get_user:
			user = await app.get_users(get_user)
	except PeerIdInvalid:
		return await app.send_edit(m, "I don't know that User.", mono=True)

	pfp = await app.get_profile_photos(user.id)
	if not pfp:
		await app.send_edit(
			m.chat.id,
			infotext.format(
				FullName(user),
				user.id,
				user.first_name,
				user.id,
				f"@{user.username}" if user.username else "",
				user.dc_id
			),
		disable_web_page_preview=True,
		)
	else:
		await app.send_cached_media(
			m.chat.id, 
			file_id = pfp[0].file_id,
			caption=infotext.format(
				FullName(user),
				user.id,
				user.first_name,
				user.id,
				f"@{user.username}" if user.username else  "",
				user.dc_id
			)
		)
		await msg.delete()
		




@app.on_message(gen("id"))
async def id(_, m: Message):
	await app.send_edit(m, "Getting id . . .", mono=True)
	cmd = m.command
	reply = m.reply_to_message

	if not reply and len(cmd) == 1:
		get_user = m.from_user.id
	elif reply and len(cmd) == 1:
		get_user = reply.from_user.id
	elif len(cmd) > 1:
		get_user = cmd[1]

	try:
		user = await app.get_users(get_user)
		chat = await app.get_chat(m.chat.id)
	except PeerIdInvalid:
		return await app.send_edit(m, "I don't know that User.", mono=True)

	u_name = user.first_name if user.first_name else None
	c_name = chat.first_name if chat.first_name else chat.title

	await app.send_edit(m, f"**{u_name}:** `{user.id}`\n**{c_name}:** `{chat.id}`")




@app.on_message(gen(["men", "mention"]))
async def mention_user(_, m: Message):
	if app.long(m) < 3:
		return await app.send_edit(m, "Incorrect input.\n\n**Example** : `.men @beastzx CTO`")

	try:
		user = await app.get_users(m.command[1])
	except Exception as e:
		await app.send_edit(m, "User not found !", mono=True)
		return await app.error(m, e)

	mention = men(user.id, " ".join(m.command[2:]))
	await app.send_edit(m, mention)




@app.on_message(gen("uinfo"))
async def get_full_user_info(_, m: Message):
	msg = await app.send_edit(m, "scrapping info . . .", mono=True)
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
		duo = f"**1. ID:** `{user.id}`\n"
		duo += f"**2. NAME:** `{user.first_name}`\n"
		duo += f"**3. DC ID:** `{user.dc_id}`\n"
		duo += f"**4. BOT:** `{user.is_bot}`\n"
		duo += f"**5. FAKE:** `{user.is_fake}`\n"
		duo += f"**6. SCAM:** `{user.is_scam}`\n"
		duo += f"**7. NAME:** `{user.first_name}`\n"
		duo += f"**8. STATUS:** `{user.status}`\n"
		duo += f"**9. IS IT ME:** `{user.is_self}`\n"
		duo += f"**10. DELETED:** `{user.is_deleted}`\n"
		duo += f"**11. CONTACT:** `{user.is_contact}`\n"
		duo += f"**12. VERIFIED:** `{user.is_verified}`\n"
		duo += f"**13. RESTRICTED:** `{user.is_restricted}`\n"

		if p_id:
			await app.send_cached_media(
				m.chat.id, 
				file_id=p_id, 
				caption=duo
			)
			await msg.delete()
		elif p_id is False:
			await app.send_edit(m, duo)
	except Exception as e:
		await app.send_edit(m, "Try again later . . .", mono=True)
		await app.error(m, e)




@app.on_message(gen(["sc", "scan"]))
async def tg_scanner(_, m: Message):
	if m.reply_to_message:
		await m.edit("Checking database . . .")
		await app.forward_messages(
			"@tgscanrobot", 
			m.chat.id, 
			m.reply_to_message.message_id
			)
		time.sleep(0.5)
		msg = await app.get_history(
			"@tgscanrobot", 
			limit=1
			)
		if msg:
			user = "**INFO: **" + msg[0].text.split("\n\n1. ")[0]
			await app.send_edit(m, user)
		else:
			await app.send_edit(m, "No information found !", mono=True)

	else:
		await app.send_edit(m, "reply to someone's message . . .", delme=2, mono=True)




@app.on_message(gen("block"))
async def block_pm(_, m: Message):
	reply = m.reply_to_message

	if app.long(m) >= 2 and not reply:
		user = m.command[1]
		try:
			await app.block_user(user)
			await app.send_edit(m, "Blocked User 🚫", mono=True, delme=3)
		except Exception as e:
			await app.error(m, e)
	elif reply:
		user = reply.from_user.id
		try:
			await app.block_user(user)
			await app.send_edit(m, "Blocked User 🚫", mono=True, delme=3)
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen("unblock"))
async def unblock_pm(_, m: Message):
	reply = m.reply_to_message

	if app.long(m) >= 2 and not reply:
		user = m.command[1]
		try:
			await app.unblock_user(user)
			await app.send_edit(m, "Unblocked User 🎉", mono=True, delme=3)
		except Exception as e:
			await app.error(m, e)
	elif reply:
		user = reply.from_user.id
		try:
			await app.unblock_user(user)
			await app.send_edit(m, "Unblocked User 🎉", mono=True, delme=3)
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen("sg"))
async def check_name_history(_, m: Message):
	reply = m.reply_to_message

	if not reply:
		await app.send_edit(m, "Reply to a user to get history of name / username.", mono=True, delme=2)

	elif reply:
		await app.send_edit(m, "Checking History...", mono=True)
		await app.forward_messages(
			"@SangMataInfo_bot", 
			m.chat.id, 
			reply.message_id
			)
		is_no_record = False
		for x in range(8):
			time.sleep(1)
			msg = await app.get_history(
				"@SangMataInfo_bot", 
				limit=3
				)
			if msg[0].text == "No records found":
				await app.send_edit(m, "No records found")
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
		if app.long(m) <= 4096 and len(text) + len("\n\n**Username History**\n\n") + len(username_history) <= 4906:
			text += "\n\n**Username History**\n\n" + username_history
			await app.send_edit(m, text)
		else:
			await app.send_edit(m, text)
			await app.send_edit(m, "\n\n**Username History**\n\n" + username_history)
		return




@app.on_message(gen("set"))
async def update_profile(_, m: Message):
	custom = m.command

	if app.long(m) < 3:
		return await app.send_edit(m, "Please use text and suffix after command ...")
	# set -> fname, lname & bio
	if app.long(m) > 2:
		text = m.text.split(None, 2)[2]

		if custom[1] in ["fname", "lname", "bio"]:
			await setprofile(
				m, 
				custom[1], 
				f"{text[2:]}"
			)
		elif custom[1] == "uname":
			await app.update_username(f"{custom[2]}"
)
	else:
		return await app.send_edit(m, f"Please specify a correct suffix.", delme=2)




@app.on_message(gen("rem"))
async def remove_profile(_, m: Message):
	if app.long(m) > 1:
		cmd = m.command[1]
	elif app.long(m) == 1:
		return await app.send_edit(m,"what do you want to remove ?", delme=2)
	try:
		if cmd in ["lname", "bio", "pfp", "uname"]:
			await rmprofile(m, cmd)
		else:
			await app.send_edit(m,"please use from the list:\n\n`lname`\n`bio`\n`pfp`\n`uname`", delme=2)
	except Exception as e:
		await app.error(m, e)




# set your profile stuffs 
async def setprofile(m: Message, args, kwargs):
	# set first name
	if args == "fname":
		try:
			await app.update_profile(
				first_name = f"{kwargs}"
				)
			await app.send_edit(
				m, 
				f"✅ Updated first name to [ {kwargs} ]"
				)
		except Exception as e:
			await app.error(m, e)
	# set last name
	elif args == "lname":
		try:
			await app.update_profile(
				last_name = f"{kwargs}"
			)
			await app.send_edit(
				m, 
				f"✅ Updated last name to [ {kwargs} ]"
				)
		except Exception as e:
			await app.error(m, e)
	# set bio
	elif args == "bio":
		try:
			await app.update_profile(
				bio = f"{kwargs}"
				)
			await app.send_edit(
				m, 
				f"✅ Updated bio to [ {kwargs}]"
				)
		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, "Please give correct format.", delme=2)




# lost everything
async def rmprofile(m: Message, args):
	# delete last name
	if args == "lname":
		await app.update_profile(
			last_name = ""
			)
		await app.send_edit(
			m, 
			"✅ Removed last name from profile."
			)
	# delete bio
	elif args == "bio":
		await app.update_profile(
			bio = "")
		await app.send_edit(
			m, 
			"✅ Removed bio from profile."
			)
	# delete profile picture
	elif args == "pfp":
		photos = await app.get_profile_photos("me")
		if photos:
			await app.delete_profile_photos([p.file_id for p in photos[1:]])
			await app.send_edit(
				m, 
				"✅ Deleted all photos from profile."
				)
		else:
			await app.send_edit(m, "❌ There are no photos in your profile.")
	# delete username
	elif args == "uname":
		await app.update_username("")
		await app.send_edit(
			m, 
			"✅ Removed username from profile."
			)
	else:
		await app.send_edit(m, "Give correct format.", delme=2)




@app.on_message(gen("repo"))
async def get_repo_link(_, m: Message):
	await app.send_edit(m, "[Here Is Tronuserbot Repo](https://github.com/beastzx18/Tron)")


