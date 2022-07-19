import re
import os
import html
import math
import json
import shlex
import random
import asyncio
import aiohttp 

from time import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

from typing import List, Union

# exceptions
from pyrogram.types import Message, User, InlineKeyboardButton
from pyrogram.errors import MessageNotModified, FloodWait

from aiohttp.client_exceptions import ContentTypeError




class Types(object):
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



class AioHttp(Types):
	@staticmethod
	async def GetRequest(link: str="", resptype: str=""):
		""" args:
				link: str = ""
				resptype: str = "json"
    
				Note: resptype is 'json' by default
					available args for restype:
					'json', 'text', 'jsontext', 'raw', 'url'
		"""
		async with aiohttp.ClientSession() as session:
			async with session.get(link) as resp:
				stored = {"json":"json", "text":"text", "jsontext":"text", "raw":"read", "url":"url"}
				try:
					returntype = resptype if resptype and resptype in stored.keys() else stored.get("json")
					if returntype == "jsontext":
						return json.loads(await resp.text())
					return await getattr(resp, returntype, None)()
				except ContentTypeError:
					return json.loads(await resp.text())



class Utilities(AioHttp):
	def HelpDex(self, page_number, allmodules, prefix):
		rows = 4
		column = 2
		help_modules = []
		for mod in allmodules:
			if not mod.startswith("_"):
				help_modules.append(mod)
		help_modules = sorted(help_modules)
		modules = [
			InlineKeyboardButton(
				text="{} {}".format(
					self.HelpEmoji(),
					x.replace("_", " ").title(),
				),
				callback_data="pluginlist-{}|{}".format(x, page_number),
			)
			for x in help_modules
		]
		twins = list(zip(modules[::column], modules[1::column]))
		if len(modules) % column == 1:
			twins.append((modules[-1],))
		num_pages = math.ceil(len(twins) / rows)
		mod_page = page_number % num_pages
		if len(twins) > rows:
			twins = twins[
				mod_page * rows : rows * (mod_page + 1)
			] + [
				(
					InlineKeyboardButton(
						text="❰ Prev",
						callback_data="{}-prev({})".format(
							prefix, mod_page
						),
					),
					InlineKeyboardButton(text="Back", callback_data=f"home-tab"),
					InlineKeyboardButton(
						text="Next ❱",
						callback_data="{}-next({})".format(
							prefix, mod_page
						),
					),
				)
			]
		return twins


	def GetMessageType(self, msg, include_text=True):
		content = None
		message_type = None
	
		if include_text is True:
			if msg.text or msg.caption:
				content = msg
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


	def GetNoteType(self, msg):
		reply = msg.reply_to_message
		note_name = None
		message_type = None
		content = None
		text = None
		file_id = None 


		if self.long() == 1:
			return None, None, None, None, None

		if msg.text:
			raw_text = msg.text.markdown 
		elif msg.caption:
			raw_text = msg.caption.markdown
		else:
			raw_text = None

		note_name = raw_text.split()[1]

		# determine what the contents of the filter are - text, image, sticker, etc
		if self.long() >= 3:
			text = raw_text.split(None, 2)[2]
			message_type = Types.TEXT

		elif reply:
			if reply.text:
				text = reply.text.markdown if reply.text else reply.caption.markdown if reply.caption else ""
				message_type = Types.TEXT
				content, message_type = self.GetMessageType(reply, include_text=False)
			else:
				return

		return note_name, text, message_type, content


	def FetchNoteType(self, msg):
		message_type = None
		content = None
		note_name = None
		text = None

		if msg:
			if msg.text:
				text = msg.text.markdown if msg.text else msg.caption.markdown if msg.caption else ""        
				message_type = Types.TEXT

			content, message_type = self.GetMessageType(msg, include_text=False)

		return note_name, text, message_type, content 


	async def IsAdmin(self, privileges):
		"""Check if we are an admin."""
		if not self.m.from_user:
			return False
		resp = (await self.m.chat.get_member("me")).privileges
		if resp is None:
			return False

		return True if getattr(resp, privileges) else False


	async def IsReply(self, msg: Message):
		"""Check if the message is a reply to another user."""
		return True if msg.reply_to_message is True else False
		

	def ClearString(self, msg: str):
		msg = re.sub(r"\<code\>(.*)\<\/code\>", "\g<1>", msg)
		msg = re.sub(r"\<i\>(.*)\<\/i\>", "\g<1>", msg)
		msg = re.sub(r"\<b\>(.*)\<\/b\>", "\g<1>", msg)
		msg = re.sub(r"\<u\>(.*)\<\/u\>", "\g<1>", msg)
		msg = re.sub(r"\*\*(.*)\*\*", "\g<1>", msg)
		msg = re.sub(r"\_\_(.*)\_\_", "\g<1>", msg)
		msg = re.sub(r"\`(.*)\`", "\g<1>", msg)
		return msg


	def QuoteHtml(self, text: str) -> str:
		"""
		Escape unexpected HTML characters.
		:param text: Original text
		:return:
		"""
		return html.escape(text, quote=False)


	def TimeFormator(self, milliseconds: int) -> str:
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


	def HumanBytes(self, size: int) -> str:
		""" converts bytes into human readable format """
		if not size:
			return ""
		power = 2 ** 10
		number = 0
		dict_power_n = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
		while size > power:
			size /= power
			number += 1
		return str(round(size, 2)) + " " + dict_power_n[number] + "B"


	async def ProgressForPyrogram(self, current, total, ud_type, message, start):
		""" generic progress display for Telegram Upload / Download status """
		now = time()
		diff = now - start
		if round(diff % 10.00) == 0 or current == total:
			# if round(current / total * 100, 0) % 5 == 0:
			percentage = current * 100 / total
			speed = current / diff
			elapsed_time = round(diff) * 1000
			time_to_completion = round((total - current) / speed) * 1000
			estimated_total_time = elapsed_time + time_to_completion

			elapsed_time = self.TimeFormator(milliseconds=elapsed_time)
			estimated_total_time = self.TimeFormator(milliseconds=estimated_total_time)

			progress = "**[{0}{1}]** \n**Progress**: __{2}%__\n".format(
				"".join(["●" for i in range(math.floor(percentage / 5))]),
				"".join(["○" for i in range(20 - math.floor(percentage / 5))]),
				round(percentage, 2),
			)

			tmp = progress + "**Done:** __{0} of {1}__\n**Speed:** __{2}/s__\n**ETA:** __{3}__\n".format(
				self.HumanBytes(current),
				self.HumanBytes(total),
				self.HumanBytes(speed),
				estimated_total_time if estimated_total_time != "" else "0 s",
			)
			try:
				await message.edit(f"{ud_type}\n {tmp}")
			except (MessageNotModified, FloodWait):
				pass


	def DictSizeInBytes(self, directory):
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

					total += self.DictSizeInBytes(entry.path)
		except NotADirectoryError:
			# if `directory` isn't a directory, get the file size then
			return os.path.getsize(directory)
		except PermissionError:
			# if for whatever reason we can't open the folder, return 0
			return 0
		return total


	def SizeFormat(self, b, factor=1024, suffix="B"):
		for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
			if b < factor:
				return f"{b:.2f}{unit}{suffix}"
			b /= factor
		return f"{b:.2f}Y{suffix}"


	def DictSize(self, location):
		return self.SizeFormat(self.DictSizeInBytes(location))


	def CleanHtml(self, raw_html):
		cleanr = re.compile("<.*?>")
		cleantext = re.sub(cleanr, "", raw_html)
		return cleantext


	def EscapeMarkdown(self, text):
		escape_chars = r"\*_`\["
		return re.sub(r"([%s])" % escape_chars, r"\\\1", text)


	def MentionHtml(self, user_id, name):
		return u'<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))


	def MentionMarkdown(self, user_id, name):
		return u'[{}](tg://user?id={})'.format(self.EscapeMarkdown(name), user_id)


	def ParseButton(self, text):
		markdown_note = text
		prev = 0
		note_data = ""
		buttons = []
		BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")
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


	def BuildKeyboard(self, buttons):
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


	def TimeParser(self, start, end=None) -> int:
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


	def ConvertSize(self, size_bytes):
		if size_bytes == 0:
			return "0B"
		size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
		i = int(math.floor(math.log(size_bytes, 1024)))
		p = math.pow(1024, i)
		s = round(size_bytes / p, 2)
		return "%s %s" % (s, size_name[i])


	def GetArgs(self):
		reply = self.m.reply_to_message
		if reply:
			return reply
		elif not reply:
			if self.long() > 1:
				return self.m
		return type("argclass", (object,), {"text" : None})()


	def SpeedConvert(self, bytesize) -> str:
		" converts bytes into kb, mb, gb, tb "
		power = 2**10 # 1024
		zero = 0
		units = {
			0: '',
			1: 'Kb/s',
			2: 'Mb/s',
			3: 'Gb/s',
			4: 'Tb/s'}
		while bytesize > power:
			bytesize /= power
			zero += 1
		return f"{round(bytesize, 2)} {units[zero]}"


	def GetReadableTime(self, seconds: int) -> str:
		" get time formated from seconds "
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


	def GenTgThumb(self, downloaded_file_name: str) -> str:
		" generates thumbnail of downloaded telegram media "
		Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
		metadata = extractMetadata(createParser(downloaded_file_name))
		height = 0
		if metadata.has("height"):
			height = metadata.get("height")
		img = Image.open(downloaded_file_name)
		img.resize((320, height))
		img.save(downloaded_file_name, "JPEG")
		return downloaded_file_name


	async def IsThumbExists(self, file_name: str):
		" get thumbnail of file if it exists "
		thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
		if os.path.exists(thumb_image_path):
			thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
		elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
			metadata = extractMetadata(createParser(file_name))
			duration = 0
			if metadata.has("duration"):
				duration = metadata.get("duration").seconds
			# get a random TTL from the duration
			ttl = str(random.randint(0, duration - 1))

			thumb_image_path = self.GenTgThumb(file_name)
		else:
			thumb_image_path = None
		return thumb_image_path


	async def RunCommand(self, shell_command: List) -> str:
		" run shell commands "
		process = await asyncio.create_subprocess_exec(
			*shell_command,
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.PIPE,
		)
		stdout, stderr = await process.communicate()
		e_response = stderr.decode().strip()
		t_response = stdout.decode().strip()
		return t_response, e_response


	async def ExtractUser(self, msg: Message) -> Union[int, str]:
		"""extracts the user from a message"""
		user_id = None
		first_name = None
		reply = msg.reply_to_message

		if reply:
			if reply.from_user:
				user_id = reply.from_user.id
				first_name = reply.from_user.first_name

		elif not reply:
			if msg.from_user:
				user_id = msg.from_user.id
				first_name = msg.from_user.first_name

		return user_id, first_name


	def ChatType(self, m: Message):
		" get chat type "
		return m.chat.type


	def FormatText(self, text, format=[]):
		" get formated text (html) "
		for x in format:
			format_dict = {
			"mono" : f"<code>{text}</code>", 
			"bold" : f"<b>{text}</b>",
			"italic" : f"<i>{text}</i>",
			"strike" : f"<s>{text}</s>",
			"underline" : f"<u>{text}</u>"
			}
			text = format_dict.get(x)
		return text


	async def HasteBinPaste(self, text):
		" paste anything to pasting site "
		try:
			async with aiohttp.ClientSession() as session:
				async with session.post(
					"https://www.toptal.com/developers/hastebin/documents", data=text.encode("utf-8"), timeout=3
					) as response:
					key = (await response.json())["key"]
					url = f"https://hastebin.com/raw/{key}"
					return url if key else None
		except Exception as e:
			await self.error(e)
