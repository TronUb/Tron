import pytz
import datetime
import time
import os
import asyncio
import traceback

from pyrogram import Client
from pyrogram.types import Message

from tronx import (
	app,
	log,
	PREFIX,
	CMD_HELP,
)

from config import Config

from .user import mymention




# date
def showdate():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_date = datetime.datetime.now(today)
	mydate = get_date.strftime("%d %b %Y")
	return mydate


# time
def showtime():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_time = datetime.datetime.now(today)
	mytime = get_time.strftime("%r")
	return mytime


# send or edit msg
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
	try:
		await m.edit(
			text, 
			parse_mode=parse_mode, 
			disable_web_page_preview=disable_web_page_preview,
		)
	except:
		await app.send_message(
			m.chat.id,
			text,
			disable_web_page_preview=disable_web_page_preview,
			parse_mode=parse_mode
		)




# send msg
async def sendmsg(m: Message, text):
	try:
		await app.send_message(
			m.chat.id,
			text
		)
	except Exception as e:
		await error(m, e)
	return


# show error
async def error(m: Message, e):
	teks = f"Traceback Report:\n\n"
	teks += f"Date: {showdate()}\nTime: {showtime()}\n\n"
	teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
	teks += f"Command: {m.text}\n\n"
	teks += f"Error:\n\n"
	teks += f"{e}\n\n"
	try:
		await app.send_message(
			Config.LOG_CHAT,
			teks
		)
		print(teks)
	except:
		print(teks)
	log.error("Please check your logs online !")
	return 




async def sleep(m: Message, sec, del_msg=False):
	await asyncio.sleep(sec)
	if del_msg:
		await m.delete()
	return




# delete msg
async def delete(m: Message, sec: int = 0):
	if not sec > 600: # 10 min
		asyncio.create_task(sleep(m, sec=sec, del_msg=True))
	else:
		log.error("maximum sleep of 10 ( 600 sec ) minutes")
	return




# plugin information (CMD_HELP)
async def data(plug):
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




# disallow use of cmds in private (user) chats
async def private(m : Message, back=True):
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
	try:
		my_codes
	except Exception as e:
		await error(m, e)



# it is equal to --> len(message.text.split())
def long(m: Message):
	text = len(m.command)
	return text if text else None




# file creator
async def create_file(m: Message, filename, text):
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



# remove multiples of same element from a list
def rem_dual(one, two):
	data = list(set(one) - set(two))
	return data



# kick users from a chat
async def kick(chat_id, user_id):
	try:
		await app.kick_chat_member(
			chat_id,
			user_id
			)
	except Exception as e:
		print(e)
		await error(m, e)



# True if string else False
def is_str(element):
	check = isinstance(element, str)
	return check



# True if boolean else False
def is_bool(element):
	check = isinstance(element, bool)
	return check



# True if float else False
def is_float(element):
	check = isinstance(element, float)
	return check



# True if integer else False
def is_int(element):
	check = isinstance(element, int)
	return check



# 
async def textlen(m: Message, one: int = 1):
	try:
		cmd = True if len(m.command) > one else False
		text = True if len(m.text) <=4096 else False
		if cmd is False:
			await send_edit(m, "Please give me some suffix . . .", mono=True, delme=3)
		elif text is False:
			await send_edit(m, "Only 4096 charactors are allowed !", mono=True, delme=3)
		else: 
			return False
	except Exception as e:
		print(e)
		await error(m, e)
