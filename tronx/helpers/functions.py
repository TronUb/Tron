import pytz
import datetime
import time
import os
import asyncio
import traceback
import requests

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import YouBlockedUser, MessageIdInvalid

from tronx import (
	app,
	log,
	PREFIX,
	CMD_HELP,
	BOT_USERNAME,
	Config,
)

from .user import mymention

from tronx.database.postgres import dv_sql as dv




def showdate():
	"""Your location's date"""
	today = pytz.timezone(Config.TIME_ZONE)
	get_date = datetime.datetime.now(today)
	mydate = get_date.strftime("%d %b %Y")
	return mydate


def showtime():
	"""Your location's time"""
	today = pytz.timezone(Config.TIME_ZONE)
	get_time = datetime.datetime.now(today)
	mytime = get_time.strftime("%r")
	return mytime


async def send_edit(
	m: Message, 
	text, 
	parse_mode="combined", 
	disable_web_page_preview=False,
	delme : int=0,
	mono=False,
	bold=False,
	italic=False,
	strike=False,
	underline=False,
	):
	"""This function edits or sends the message"""

	mono_text = f"<code>{text}</code>"
	bold_text = f"<b>{text}</b>"
	italic_text = f"<i>{text}</i>"
	strike_through_text = f"<s>{text}</s>"
	underline_text = f"<u>{text}</u>"

	if mono:
		await edit_text(
			m, 
			mono_text, 
			disable_web_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)
	elif bold:
		await edit_text(
			m, 
			bold_text, 
			disable_web_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)
	elif italic:
		await edit_text(
			m, 
			italic_text, 
			disable_web_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)
	elif strike:
		await edit_text(
			m, 
			strike_through_text, 
			disable_web_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)
	elif underline:
		await edit_text(
			m, 
			underline_text, 
			disable_wab_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)
	else:
		await edit_text(
			m, 
			text, 
			disable_web_page_preview=disable_web_page_preview, 
			parse_mode=parse_mode
		)

	try:
		if delme != 0:
			asyncio.create_task(sleep(m, sec=delme, del_msg=True))

	except Exception as e:
		await error(m, e)


async def edit_text(m: Message, text, disable_web_page_preview=False, parse_mode="combined"):
	"""edit or send that message"""
	try:
		await m.edit(
			text, 
			parse_mode=parse_mode, 
			disable_web_page_preview=disable_web_page_preview,
		)
	except MessageIdInvalid:
		await app.send_message(
			m.chat.id,
			text,
			disable_web_page_preview=disable_web_page_preview,
			parse_mode=parse_mode
		)


async def sendmsg(m: Message, text):
	"""Send message"""
	try:
		await app.send_message(
			m.chat.id,
			text
		)
	except Exception as e:
		await error(m, e)


async def error(m: Message, e):
	"""Error tracing"""
	teks = f"Traceback Report:\n\n"
	teks += f"Date: {showdate()}\nTime: {showtime()}\n\n"
	teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
	teks += f"Command: {m.text}\n\n"
	teks += f"Error:\n\n"
	teks += f"**SHORT:** \n\n{e}\n\n"
	teks += f"**FULL:** \n\n{traceback.format_exc()}"
	try:
		await app.send_message(
			Config.LOG_CHAT,
			teks
		)
	except PeerIdInvalid:
		print(teks)
	log.error("Please check your logs online.")


async def sleep(m: Message, sec, del_msg=False):
	"""Delete a message after some time"""
	await asyncio.sleep(sec)
	if del_msg:
		await m.delete()


async def delete(m: Message, sec: int = 0):
	"""Delete a message after some time using sleep func"""
	if not sec > 600: # 10 min
		asyncio.create_task(sleep(m, sec=sec, del_msg=True))
	else:
		log.error("Delete function can sleep for 10 ( 600 sec ) minutes")


async def data(plug):
	"""Create help information page for each module"""
	try:
		plugin_data = []
		plugin_data.clear()

		for x, y in zip(
			CMD_HELP.get(plug)[1].keys(), 
			CMD_HELP.get(plug)[1].values()
			):
			plugin_data.append(
				f"CMD: `{PREFIX}{x}`\nINFO: `{y}`\n\n"
				)
		return plugin_data
	except Exception as e:
		print(e)
		return None


async def private(m : Message, back=True):
	"""Warn if command used group is private"""
	if m.chat.type == "private":
		await send_edit(
			m, 
			"Please use these commands in groups . . .",
			mono=True, 
			delme=True
		)
		if back:
			return


async def code(my_codes):
	"""noobie code"""
	try:
		my_codes
	except Exception as e:
		await error(m, e)


def long(m: Message):
	"""to check args, same as len(message.text.split())"""
	text = len(m.command)
	return text if text else None


async def create_file(m: Message, filename, text):
	"""Create any file with any extension"""
	try:
		name = filename
		content = text
		file = open(name, "w+")
		file.write(content)
		file.close()
		await app.send_document(
			m.chat.id,
			name,
			caption = f"**Uploaded By:** {mymention()}"
			)
		os.remove(name)
		await m.delete()
	except Exception as e:
		await error(m, e)


def rem_dual(one, two):
	"""remove multiples of same element from a list"""
	data = list(set(one) - set(two))
	return data


async def kick(chat_id, user_id):
	"""kick user from chat"""
	try:
		await app.kick_chat_member(
			chat_id,
			user_id
			)
	except Exception as e:
		print(e)


def is_str(element):
	"""True if string else False"""
	check = isinstance(element, str)
	return check


def is_bool(element):
	"""True if boolean else False"""
	check = isinstance(element, bool)
	return check


def is_float(element):
	"""True if float else False"""
	check = isinstance(element, float)
	return check


def is_int(element):
	"""True if int else False"""
	check = isinstance(element, int)
	return check


async def textlen(m: Message, num: int = 1):
	"""auto check and warn if not suffix with command"""
	try:
		cmd = True if len(m.command) > num else False
		text = True if len(m.text) > 1 and len(m.text) <= 4096 else False
		if cmd is False:
			await send_edit(m, "Please give me some suffix . . .", mono=True, delme=3)
		elif text is False:
			await send_edit(m, "Only 4096 characters are allowed !", mono=True, delme=3)
		else: 
			return False
	except Exception as e:
		print(e)
		await error(m, e)


async def get_last_msg(m: Message, user_id: int, reverse=False):
	"""Get the first or last message of user chat"""
	if reverse:
		data = await app.get_history(user_id, limit=1, reverse=True)
	else:
		data = await app.get_history(user_id, limit=1)
	return data


async def toggle_inline(m: Message):
	"""Turn on | off inline mode of your bot"""
	try:
		await send_edit(m, "Processing command . . .", mono=True)
		await app.send_message("BotFather", "/mybots") # BotFather (93372553) 
		await asyncio.sleep(1) # floodwaits

		data = await get_last_msg(m)
		usernames = list(data[0].reply_markup.inline_keyboard)[0]

		unames = []
		unames.clear()

		for x in usernames:
			unames.append(x.text)

		await send_edit(m, "Choosing bot . . . ", mono=True)

		if BOT_USERNAME in unames:
			await data[0].click(BOT_USERNAME)
		else:
			return await send_edit(m, "Looks like you don't have a bot please, use your own bot . . .", mono=True, delme=True)

		data = await get_last_msg(m)

		await send_edit(m, "Pressing Bot Settings . . . ", mono=True)

		await data[0].click("Bot Settings")

		data = await get_last_msg(m)

		await send_edit(m, "checking whether inline mode is On or Off . . . ", mono=True)

		await data[0].click("Inline Mode")

		data = await get_last_msg(m)

		# Turn on inline mode
		if "Turn on" in str(data[0]):
			await send_edit(m, "Turning Inline mode on . . . ", mono=True)
			await data[0].click("Turn on")
			await send_edit(m, "Inline mode is now turned On.", mono=True, delme=True)
		# Turn inline mode off
		elif "Turn inline mode off" in str(data[0]):
			await send_edit(m, "Turning Inline mode Off . . .", mono=True)
			await data[0].click("Turn inline mode off")
			await send_edit(m, "Inline mode is now turned Off.", mono=True, delme=True)
	except YouBlockedUser:
		await app.unblock_user("BotFather")
		await toggle_inline(m)
	except Exception as e:
		await error(m, e)


def quote():
	"""anime quotes for weebs"""
	results = requests.get("https://animechan.vercel.app/api/random").json()
	msg = f"❝ {results.get('quote')} ❞"
	msg += f" [ {results.get('anime')} ]\n\n"
	msg += f"- {results.get('character')}\n\n"
	return msg


def ialive_pic():
	"""inline alive pic url"""
	pic_url = dv.getdv("USER_PIC")
	data = pic_url if pic_url else Config.USER_PIC
	return data if data else None


