import time
import re
import shlex
import os
import asyncio
import html
import math
import aiohttp 
import random
import json

from time import sleep
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

from math import ceil
from typing import List, Union
from re import escape, sub
from enum import IntEnum, unique

from tronx import (
	app, 
	USER_ID,
	Config,
)

from pyrogram.types import Message, User, InlineKeyboardButton
from pyrogram.errors import RPCError, MessageNotModified, FloodWait




HELP_EMOJI = " "
LAYER_FEED_CHAT = None
LAYER_UPDATE_INTERVAL = None
LAYER_UPDATE_MESSAGE_CAPTION = None
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")




@unique
class Types(IntEnum):
	TEXT = 1
	DOCUMENT = 2
	PHOTO = 3
	VIDEO = 4
	STICKER = 5
	AUDIO = 6
	VOICE = 7
	VIDEO_NOTE = 8
	ANIMATION = 9
	ANIMATED_STICKER = 10
	CONTACT = 11




# help menu builder
def helpdex(page_number, loaded_modules, prefix):
	rows = 4
	column = 2
	help_modules = []
	for mod in loaded_modules:
		if not mod.startswith("_"):
			help_modules.append(mod)
	help_modules = sorted(help_modules)
	modules = [
		InlineKeyboardButton(
			text="{} {}".format(
				HELP_EMOJI,
				x.replace("_", " ").title(),
			),
			callback_data="modulelist_{}|{}".format(x, page_number),
		)
		for x in help_modules
	]
	twins = list(zip(modules[::column], modules[1::column]))
	if len(modules) % column == 1:
		twins.append((modules[-1],))
	num_pages = ceil(len(twins) / rows)
	mod_page = page_number % num_pages
	if len(twins) > rows:
		twins = twins[
			mod_page * rows : rows * (mod_page + 1)
		] + [
			(
				InlineKeyboardButton(
					text="❰ Prev",
					callback_data="{}_prev({})".format(
						prefix, mod_page
					),
				),
				InlineKeyboardButton(text="Back", callback_data=f"open-start-dex"),
				InlineKeyboardButton(
					text="Next ❱",
					callback_data="{}_next({})".format(
						prefix, mod_page
					),
				),
			)
		]
	return twins




# get type of message
def get_message_type(msg, include_text=True):
	content = None
	message_type = None
	
	if include_text is True:
		if msg.text or msg.caption:
			content = None
			message_type = Types.TEXT

	elif msg.sticker:
		content = msg.sticker.file_id
		message_type = Types.STICKER

	elif msg.document:
		if msg.document.mime_type == "application/x-bad-tgsticker":
			message_type = Types.ANIMATED_STICKER
		else:
			message_type = Types.DOCUMENT
		content = msg.document.file_id

	elif msg.photo:
		content = msg.photo.file_id  # last elem = best quality
		message_type = Types.PHOTO

	elif msg.audio:
		content = msg.audio.file_id
		message_type = Types.AUDIO

	elif msg.voice:
		content = msg.voice.file_id
		message_type = Types.VOICE

	elif msg.video:
		content = msg.video.file_id
		message_type = Types.VIDEO

	elif msg.video_note:
		content = msg.video_note.file_id
		message_type = Types.VIDEO_NOTE

	elif msg.animation:
		content = msg.animation.file_id
		message_type = Types.ANIMATION
	return content, message_type




def get_note_type(msg):
	reply = msg.reply_to_message
	note_name = None
	message_type = None
	content = None
	text = None
	file_id = None


	if long(m) <= 1:
		return None, None, None, None, None

	if msg.text:
		raw_text = msg.text.markdown 
	else:
		raw_text = msg.caption.markdown
	note_name = raw_text.split()[1]

	# determine what the contents of the filter are - text, image, sticker, etc
	if long(m) >= 3:
		text = raw_text.split(None, 2)[2]
		message_type = Types.TEXT

	elif reply:
		if reply.text:
			text = reply.text.markdown if reply.text else reply.caption.markdown if reply.caption else ""
			message_type = Types.TEXT
		content, message_type = get_message_type(reply, include_text=False)
	else:
		return

	return note_name, text, message_type, content




def fetch_note_type(msg):
	message_type = None
	content = None
	note_name = None
	text = None

	if msg:
		if msg.text:
			text = msg.text.markdown if msg.text else msg.caption.markdown if msg.caption else ""        
			message_type = Types.TEXT

		content, message_type = get_message_type(msg, include_text=False)

	return note_name, text, message_type, content 




async def CheckAdmin(m: Message):
	"""Check if we are an admin."""

	ranks = ["administrator", "creator"]

	data = await app.get_chat_member(
		chat_id=m.chat.id, 
		user_id=m.from_user.id
	)

	return False if not data.status in ranks else True




async def CheckReplyAdmin(m: Message):
	"""Check if the message is a reply to another user."""
	if not m.reply_to_message:
		await m.edit(f"`.{m.command[0]}` needs to be a reply")
		sleep(2)
		await m.delete()
	elif m.reply_to_message.from_user.is_self:
		await m.edit(f"I can't {m.command[0]} myself.")
		sleep(2)
		await m.delete()
	else:
		return True




async def RestrictFailed(m: Message):
	await m.edit(f"I can't {message.command} this user.")
	sleep(2)
	await m.delete()



class AioHttp:
	@staticmethod
	async def get_json(link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				return await resp.json()

	@staticmethod
	async def get_text(link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				return await resp.text()

	@staticmethod
	async def get_json_from_text(link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				text = await resp.text()
				return json.loads(text)

	@staticmethod
	async def get_raw(link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				return await resp.read()

	@staticmethod
	async def get_url(link):
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				return resp.url




def clear_string(msg: str):
	msg = re.sub(r"\<code\>(.*)\<\/code\>", "\g<1>", msg)
	msg = re.sub(r"\<i\>(.*)\<\/i\>", "\g<1>", msg)
	msg = re.sub(r"\<b\>(.*)\<\/b\>", "\g<1>", msg)
	msg = re.sub(r"\<u\>(.*)\<\/u\>", "\g<1>", msg)
	msg = re.sub(r"\*\*(.*)\*\*", "\g<1>", msg)
	msg = re.sub(r"\_\_(.*)\_\_", "\g<1>", msg)
	msg = re.sub(r"\`(.*)\`", "\g<1>", msg)
	return msg




def quote_html(text: str) -> str:
	"""
	Escape unexpected HTML characters.
	:param text: Original text
	:return:
	"""
	return html.escape(text, quote=False)




async def progress_for_pyrogram(current, total, ud_type, message, start):
	""" generic progress display for Telegram Upload / Download status """
	now = time.time()
	diff = now - start
	if round(diff % 10.00) == 0 or current == total:
		# if round(current / total * 100, 0) % 5 == 0:
		percentage = current * 100 / total
		speed = current / diff
		elapsed_time = round(diff) * 1000
		time_to_completion = round((total - current) / speed) * 1000
		estimated_total_time = elapsed_time + time_to_completion

		elapsed_time = time_formatter(milliseconds=elapsed_time)
		estimated_total_time = time_formatter(milliseconds=estimated_total_time)

		progress = "**[{0}{1}]** \n**Progress**: __{2}%__\n".format(
			"".join(["●" for i in range(math.floor(percentage / 5))]),
			"".join(["○" for i in range(20 - math.floor(percentage / 5))]),
			round(percentage, 2),
		)

		tmp = progress + "**Done:** __{0} of {1}__\n**Speed:** __{2}/s__\n**ETA:** __{3}__\n".format(
			humanbytes(current),
			humanbytes(total),
			humanbytes(speed),
			estimated_total_time if estimated_total_time != "" else "0 s",
		)
		try:
			await message.edit(f"{ud_type}\n {tmp}")
		except (MessageNotModified, FloodWait):
			pass




def humanbytes(size: int) -> str:
	""" converts bytes into human readable format """
	# https://stackoverflow.com/a/49361727/4723940
	# 2**10 = 1024
	if not size:
		return ""
	power = 2 ** 10
	number = 0
	dict_power_n = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
	while size > power:
		size /= power
		number += 1
	return str(round(size, 2)) + " " + dict_power_n[number] + "B"




# --------------------------------
def get_size_recursive(directory):
	"""Returns the `directory` size in bytes."""
	total = 0
	try:
		# print("[+] Getting the size of", directory)
		for entry in os.scandir(directory):
			if entry.is_file():
				# if it's a file, use stat() function
				total += entry.stat().st_size
			elif entry.is_dir():
				# if it's a directory, recursively call this function
				total += get_size_recursive(entry.path)
	except NotADirectoryError:
		# if `directory` isn't a directory, get the file size then
		return os.path.getsize(directory)
	except PermissionError:
		# if for whatever reason we can't open the folder, return 0
		return 0
	return total




def get_size_format(b, factor=1024, suffix="B"):
	for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
		if b < factor:
			return f"{b:.2f}{unit}{suffix}"
		b /= factor
	return f"{b:.2f}Y{suffix}"




def get_directory_size(location):
	return get_size_format(get_size_recursive(location))




def cleanhtml(raw_html):
	cleanr = re.compile("<.*?>")
	cleantext = re.sub(cleanr, "", raw_html)
	return cleantext




def escape_markdown(text):
	escape_chars = r"\*_`\["
	return re.sub(r"([%s])" % escape_chars, r"\\\1", text)




def mention_html(user_id, name):
	return u'<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))




def mention_markdown(user_id, name):
	return u'[{}](tg://user?id={})'.format(escape_markdown(name), user_id)




def parse_button(text):
	markdown_note = text
	prev = 0
	note_data = ""
	buttons = []
	for match in BTN_URL_REGEX.finditer(markdown_note):
		# Check if btnurl is escaped
		n_escapes = 0
		to_check = match.start(1) - 1
		while to_check > 0 and markdown_note[to_check] == "\\":
			n_escapes += 1
			to_check -= 1
 
		# if even, not escaped -> create button
		if n_escapes % 2 == 0:
			# create a thruple with button label, url, and newline status
			buttons.append((match.group(2), match.group(3), bool(match.group(4))))
			note_data += markdown_note[prev:match.start(1)]
			prev = match.end(1)
		# if odd, escaped -> move along
		else:
			note_data += markdown_note[prev:to_check]
			prev = match.start(1) - 1
	else:
		note_data += markdown_note[prev:]

	return note_data, buttons




def build_keyboard(buttons):
	keyb = []
	keyb.clear()

	for btn in buttons:
		keyb.append(
				InlineKeyboardButton(
					btn[0],
					callback_data=btn[1]
				)
		)
	return keyb




def time_formatter(milliseconds: int) -> str:
	""" converts seconds into human readable format """
	seconds, milliseconds = divmod(int(milliseconds), 1000)
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	tmp = (
		((str(days) + "d, ") if days else "")
		+ ((str(hours) + "h, ") if hours else "")
		+ ((str(minutes) + "m, ") if minutes else "")
		+ ((str(seconds) + "s, ") if seconds else "")
		+ ((str(milliseconds) + "ms, ") if milliseconds else "")
	)
	return tmp[:-2]




def time_parser(start, end=None) -> int:
	if end is None:
		time_end = start
	else:
		time_end = end - start
	month = time_end // 2678400
	days = time_end // 86400
	hours = time_end // 3600 % 24
	minutes = time_end // 60 % 60
	seconds = time_end % 60
	times = ""
	if month:
		times += "{} month, ".format(month)
	if days:
		times += "{} days, ".format(days)
	if hours:
		times += "{} hours, ".format(hours)
	if minutes:
		times += "{} minutes, ".format(minutes)
	if seconds:
		times += "{} seconds".format(seconds)
	if times == "":
		times = "{} miliseconds".format(time_end)
	return times




def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])




def ReplyCheck(m: Message):
	reply_id = False
	reply = m.reply_to_message

	if reply:
		reply_id = reply.message_id if reply else m.message_id if not m.from_user.is_self else False

	return reply_id




def get_arg(m):
	msg = m.text
	msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
	split = msg[1:].replace("\n", " \n").split(" ")
	if " ".join(split[1:]).strip() == "":
		return ""
	return " ".join(split[1:])




def get_args(m):
	try:
		message = m.text
	except AttributeError:
		pass
	if not message:
		return False
	message = message.split(maxsplit=1)
	if len(message) <= 1:
		return []
	message = message[1]
	try:
		split = shlex.split(message)
	except ValueError:
		return message  # Cannot split, let's assume that it's just one long message
	return list(filter(lambda x: len(x) > 0, split))




def speed_convert(size):
	power = 2**10
	zero = 0
	units = {
		0: '',
		1: 'Kb/s',
		2: 'Mb/s',
		3: 'Gb/s',
		4: 'Tb/s'}
	while size > power:
		size /= power
		zero += 1
	return f"{round(size, 2)} {units[zero]}"




def get_readable_time(seconds: int) -> str:
	count = 0
	ping_time = ""
	time_list = []
	time_suffix_list = ["s", "m", "h", "days"]

	while count < 4:
		count += 1
		remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
		if seconds == 0 and remainder == 0:
			break
		time_list.append(int(result))
		seconds = int(remainder)

	for x in range(len(time_list)):
		time_list[x] = str(time_list[x]) + time_suffix_list[x]
	if len(time_list) == 4:
		ping_time += time_list.pop() + ", "

	time_list.reverse()
	ping_time += ":".join(time_list)

	return ping_time




async def is_thumb_image_exists(file_name: str):
	thumb_image_path = os.path.join(Config.TEMP_DICT, "thumb_image.jpg")
	if os.path.exists(thumb_image_path):
		thumb_image_path = os.path.join(Config.TEMP_DICT, "thumb_image.jpg")
	elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
		metadata = extractMetadata(createParser(file_name))
		duration = 0
		if metadata.has("duration"):
			duration = metadata.get("duration").seconds
		# get a random TTL from the duration
		ttl = str(random.randint(0, duration - 1))

		thumb_image_path = gen_tg_thumbnail(await take_screen_shot(file_name, ttl))
	else:
		thumb_image_path = None
	return thumb_image_path




def gen_tg_thumbnail(downloaded_file_name: str) -> str:
	Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
	metadata = extractMetadata(createParser(downloaded_file_name))
	height = 0
	if metadata.has("height"):
		height = metadata.get("height")
	img = Image.open(downloaded_file_name)
	img.resize((320, height))
	img.save(downloaded_file_name, "JPEG")
	return downloaded_file_name




async def run_command(shell_command: List) -> (str, str):
	process = await asyncio.create_subprocess_exec(
		*shell_command,
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
	)
	stdout, stderr = await process.communicate()
	e_response = stderr.decode().strip()
	t_response = stdout.decode().strip()
	return t_response, e_response




async def extract_user(m: Message) -> (int, str):
	"""extracts the user from a message"""
	user_id = None
	user_first_name = None
	reply = m.reply_to_message

	if reply:
		user_id = reply.from_user.id
		user_first_name = reply.from_user.first_name

	elif long(m) > 1:
		if long(m) > 1:
			# 0: is the command used
			# 1: should be the user specified
			required_entity = m.entities[1]
			if required_entity.type == "text_mention":
				user_id = required_entity.user.id
				user_first_name = required_entity.user.first_name
			elif required_entity.type == "mention":
				user_id = m.text[
					required_entity.offset : required_entity.offset
					+ required_entity.length
				]
				# don't want to make a request -_-
				user_first_name = user_id
		else:
			user_id = m.command[1]
			# don't want to make a request -_-
			user_first_name = user_id

	else:
		user_id = m.from_user.id
		user_first_name = m.from_user.first_name

	return (user_id, user_first_name)




def GetUserMentionable(user: User):
	""" Get mentionable text of a user."""
	if user.username:
		username = "@{}".format(user.username)
	else:
		if user.last_name:
			name_string = "{} {}".format(user.first_name, user.last_name)
		else:
			name_string = "{}".format(user.first_name)

		username = "<a href='tg://user?id={}'>{}</a>".format(user.id, name_string)

	return username




# return msg type
def types(m: Message):
	reply = m.reply_to_message
	if reply.text:
		cast = "text" 
	elif reply.photo:
		cast = "photo"
	elif reply.video:
		cast = "video"
	elif reply.document:
		cast = "document"
	elif reply.contact:
		cast = "contact"
	elif reply.audio:
		cast = "audio"
	elif reply.sticker:
		cast = "sticker"
	elif reply.animation:
		cast = "animation"
	elif reply.poll:
		cast = "poll"
	else:
		cast = "unknown"
	return cast




# chat type
def chattype(m: Message):
	return m.chat.type


