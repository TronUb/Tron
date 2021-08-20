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
	error,
)




date_dict = []




CMD_HELP.update(
    {
        "profile":f"""
**PLUGIN:** `profile`\n\n
**COMMAND:** `{PREFIX}block «username» or «reply to user»` \n**USAGE:** Block a user from sending message in your pm.\n
**COMMAND:** `{PREFIX}unblock «username» or «reply to user»` \n**USAGE:** Unblock a user and allow him to send messages in your pm.\n
**COMMAND:** `{PREFIX}repo` \n**USAGE:** Tron Userbot official repository link.\n
**COMMAND:** `{PREFIX}rem` `«lname»` or `«username` \n**USAGE:** Remove last name or username from profile, For Example: {PREFIX}rem username.\n
**COMMAND:** `{PREFIX}set` `«fname»`/`«lname»`/`«username»`/`«bio»`| `«text»` \n**USAGE:** Choose a option from command and set anything in your profile, For Example: `{PREFIX}set fname BEAST`\n
**COMMAND:** `{PREFIX}uinfo «reply to user»` \n**USAGE:** Get Full Info Of A Specific User.\nThis Command Includes More Details.\n
**COMMAND:** `{PREFIX}sc «reply to user»` \n**USAGE:**  Find Out Groups Of A Specific User, Reply To That User.\n
**COMMAND:** `{PREFIX}sang` \n**USAGE:** Get name & username history of a particular user in groups or private chats.\n
**COMMAND:** `{PREFIX}men «username» «text»` \n**USAGE:** Mention a user in a specific text.\n
**COMMAND:** `{PREFIX}mention «username» «text»` \n**USAGE:** Mention a user in a specific text, alternative command.\n
"""
    }
)




def form(text):
	if type(text) == type(int()):
		result = int
	elif type(text) == type(str()):
		result == str
	elif type(text) == type(bool()):
		result = bool
	return result




men = partial("<a href='tg://user?id={}'>{}</a>".format)


infotext = (
	"**NAME:** `{full_name}`\n"
	"**USER ID:** `{user_id}`\n"
	"**Mention:** [{full_name}](tg://user?id={user_id})\n"
	"**USERNAME:** @{username}\n"
	"**DC ID:** {dc_id}\n"
)




def ReplyCheck(m: Message):
	reply_id = None
	if m.reply_to_message:
		reply_id = m.reply_to_message.message_id
	elif not m.from_user.is_self:
		reply_id = m.message_id
	return reply_id




def FullName(user: User):
	return user.first_name + " " + user.last_name if user.last_name else user.first_name




@app.on_message(gen("whois"))
async def whois(app, m: Message):
	reply = m.reply_to_message
	await m.edit("...")
	cmd = m.command
	if reply and len(cmd) == 1:
		get_user = m.reply_to_message.id
	elif not reply and len(cmd) == 1:
		get_user = m.from_user.id
	elif len(cmd) > 1:
		get_user = cmd[1]
		if form(get_user) == int:
			users = get_user
		elif form(get_user) == str:
			users = f"@{get_user}"
		elif form(get_user) == bool:
			await m.edit(
				"Please give a valid id or username."
				)
			return
		else:
			await m.edit(
				"Something went wrong!"
				)
	try:
		user = await app.get_users(users)
	except PeerIdInvalid:
		await m.reply("I don't know that User.")
		return
	pfp = await app.get_profile_photos(user.id)
	if not pfp:
		await m.edit(
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
		dls = await app.download_media(pfp[0]["file_id"], file_name=f"{user.id}.png")
		await m.delete()
		await app.send_document(
			message.chat.id,
			dls,
			caption=infotext.format(
				full_name=FullName(user),
				user_id=user.id,
				first_name=user.first_name,
				username=user.username or "",
				dc_id=user.dc_id
			),
			reply_to_message_id=reply.message_id if reply else None,
		)
		os.remove(dls)




@app.on_message(gen("id"))
async def id(app, m: Message):
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
async def mention(app, m: Message):
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
async def get_full_user_info(app, m: Message):
	await m.edit('scrapping info...')
	try:
		user = m.reply_to_message.from_user.id
	except:
		user = m.from_user.id
	try:
		await app.send_message("@creationdatebot", f"/start")
		await asyncio.sleep(1)
		date_dict.clear()
		msg = await app.send_message("@creationdatebot", f"/id {user}")
		await asyncio.sleep(1)
		await app.send(functions.messages.DeleteHistory(peer=await app.resolve_peer(747653812), max_id=msg.chat.id))
		user_info = await app.send(
			functions.users.GetFullUser(id=await app.resolve_peer(user)))
		if user_info.user.username == None:
			username = 'None'
		else:
			username = f'@{user_info.user.username}'
		if user_info.about == None:
			about = 'None'
		else:
			about = user_info.about
		user_info = (f'''USERNAME: {username}
ID: `{user_info.user.id}`
BOT: `{user_info.user.bot}`
SCAM: `{user_info.user.scam}`
NAME: `{user_info.user.first_name}`
DELETED: `{user_info.user.deleted}`
BIO: `{about}`
CONTACT: `{user_info.user.contact}`
RESTRICTED: `{user_info.user.restricted}`
VERIFIED: `{user_info.user.verified}`
PHONE CALLS AVAILABLE:` {user_info.phone_calls_available}`
BLOCKED:` {user_info.blocked}`''')
		date_dict.clear()
		await message.edit(user_info)
	except:
		await message.edit('Error !! Please Try Again Later...')




@app.on_message(gen(["sc", "scan"]))
async def tg_scanner(app, m: Message):
	if m.reply_to_message:
		await m.edit("Checking database...")
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




@app.on_message(gen("unblock"))
async def unblock_pm(app, m: Message):
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
async def check_name_history(app, m: Message):
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
				await message.edit("No records found")
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
		text = "**Name History for** [{}](tg://user?id={}) (`{}`)\n\n".format(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.id, message.reply_to_message.from_user.id) + history_name
		if len(text) <= 4096 and len(text) + len("\n\n**Username History**\n\n") + len(username_history) <= 4906:
			text += "\n\n**Username History**\n\n" + username_history
			await m.edit(text)
		else:
			await m.edit(text)
			await m.reply("\n\n**Username History**\n\n" + username_history)
		return
	else:
		await m.edit("Reply to a user to get history of name / username."
		)




@app.on_message(gen("block"))
async def block_pm(app, m: Message):
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




@app.on_message(gen("set"))
async def update_profile(app, m: Message):
	custom = m.command[1]
	text = m.text.split(None, 2)[2]

	if len(m.command) < 2:
		await m.edit("Please use text and suffix after command ...")
		return
	# set -> fname, lname & bio
	if custom:
		if custom == "fname" or "lname" or "bio":
			await setprofile(
				m, 
				custom, 
				f"{text}"
				)
		elif custom == "uname":
			app.update_username(
				f"{text}"
				)
	else:
		await m.edit(
			f"Please specify a correct suffix."
			)
	return




@app.on_message(gen("rem"))
async def remove_profile(app, m: Message):
	if len(m.text) > 1:
		cmd = m.command[1]
	else:
		await m.edit(
			"what do you want to remove ?"
			)
	try:
		if cmd in ["lname", "bio", "pfp", "uname"]:
			await rmprofile(m, cmd)
		else:
			await m.edit(
				"please use from the list:\n\n`lname`\n`bio`\n`pfp`\n`uname`"
				)
	except Exception as e:
		await error(m, e)




@app.on_message(filters.command("repo", PREFIX) & filters.me)
async def remove_pfp(_, m: Message):
	await m.edit_text("[Here Is Tronuserbot Repo](https://github.com/beastzx18/Tron)")




# set your profile stuffs 
async def setprofile(m: Message, args, kwargs):
	if args == "fname":
		try:
			await app.update_profile(
				first_name = f"{kwargs}"
				)
			await m.edit(
				f"✅ Updated first name to [ {kwargs} ]"
				)
		except Exception as e:
			await error(m, e)
	elif args == "lname":
		try:
			await app.update_profile(
				last_name = f"{kwargs}"
			)
			await m.edit(
				f"✅ Updated last name to [ {kwargs} ]"
				)
		except Exception as e:
			await error(m, e)
	elif args == "bio":
		try:
			await app.update_profile(
				bio = f"{kwargs}"
				)
			await m.edit(
				f"✅ Updated bio to [ {kwargs}]"
				)
		except Exception as e:
			await error(m, e)
	else:
		await m.edit(
			"Please give correct format."
			)
	return




# lost everything
async def rmprofile(m: Message, args):
	if args == "lname":
		await app.update_profile(
			last_name = ""
			)
		await m.edit(
			"✅ Removed last name from profile."
			)
	elif args == "bio":
		await app.update_profile(
			bio = "")
		await m.edit(
			"✅ Removed bio from profile."
			)
	elif args == "pfp":
		photos = await app.get_profile_photos("me")
		if photos:
			await app.delete_profile_photos([p.file_id for p in photos[1:]])
			await m.edit(
				"✅ Deleted all photos from profile."
				)
		else:
			await m.edit(
				"❌ There are no photos in your profile."
				)
	elif args == "uname":
		await app.update_username("")
		await m.edit(
			"✅ Removed username from profile."
			)
	else:
		await m.edit(
			"Give correct format."
			)
	return



