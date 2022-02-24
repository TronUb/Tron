import os
import pytz
import time
import datetime
import asyncio
import traceback
import subprocess
import importlib
import requests

from typing import Union, List
from pyrogram.types import Message
from pyrogram.errors import YouBlockedUser, MessageIdInvalid, PeerIdInvalid





class Functions(object):
	async def aexec(self, m, code):
		"""
		params:
			1. message (update) :: incoming update
			2. code: str :: your written python code

		use:
			use this function to execute python codes

		ex: (async)
			await app.aexec(message, "print('Hello, World !')")
		"""

		exec(
			f"async def __aexec(self, m): "
			+ "".join(f"\n {l}" for l in code.split("\n"))
		)
		return await locals()["__aexec"](self, m)


	def showdate(self):
		"""
		params: 
			None

		use: 
			use this function to get realtime date of your location

		ex: (async)
			await app.showdate()
		"""

		today = pytz.timezone(self.TIME_ZONE)
		get_date = datetime.datetime.now(today)
		mydate = get_date.strftime("%d %b %Y")
		return mydate


	def showtime(self):
		"""
		params: 
			None

		use: 
			use this function to get time of your location

		ex: (async)
			await app.showtime()
		"""

		today = pytz.timezone(self.TIME_ZONE)
		get_time = datetime.datetime.now(today)
		mytime = get_time.strftime("%r")
		return mytime


	async def edit_text(
		self, 
		m: Message, 
		text, 
		disable_web_page_preview=False, 
		parse_mode="combined",
		reply_markup=None
		):
		"""
		params: 
			1. message :: incoming update
			2. text: str :: text to be edited to
			3. disable_web_page_preview: bool, default=False :: shows web page preview if True, Not if it is False

		use: 
			use this function to edit message, this is also a alias for send_edit function

		ex: (async)
			await app.edit_text(m, "This is a text", disable_web_page_preview=True)
		"""

		try:
			if m.from_user and m.from_user.is_self:
				m = await m.edit(
					text, 
					parse_mode=parse_mode, 
					disable_web_page_preview=disable_web_page_preview,
					reply_markup=reply_markup
				)
			elif m.from_user and not m.from_user.is_self: # for sudo users
				m = await self.send_message(
					m.chat.id,
					text,
					disable_web_page_preview=disable_web_page_preview,
					parse_mode=parse_mode,
					reply_markup=reply_markup
				)
		except Exception as e:
			self.log.info(e)
		return m


	async def error(self, m: Message, e, edit_error=False):
		"""
		params: 
			1. message (update) :: incoming updates
			2. error :: occured error
			3. edit_error: bool, default=False :: edits | sends error message 

		usage:
			use this function at the end of try/except block

		ex: (async)
			try:
				await app.send_message(message.chat.id, "This is a test")
			except Exception as e:
				await app.error(message, error, edit_error=True) 
		"""

		teks = f"**Traceback Report:**\n\n"
		teks += f"**Date:** `{self.showdate()}`\n**Time:** `{self.showtime()}`\n\n"
		teks += f"`This can be a error in tronuserbot, if you want you can forward this to @tronuserbot_support.`\n\n" 
		teks += f"**Command:** `{m.text}`\n\n"
		teks += "`-`" * 30 + "\n\n"
		teks += f"**SHORT:** \n\n`{e}`\n\n"
		teks += f"**FULL:** \n\n`{traceback.format_exc()}`"

		try:
			if edit_error:
				if hasattr(e, "MESSAGE"):
					await self.send_edit(m, f"[ **{e.CODE}** ] : `{e.MESSAGE}`")
				else:
					await self.send_edit(m, e.args)

			await self.send_message(self.LOG_CHAT, teks)

		except PeerIdInvalid:
			self.log.error(teks)
		except Exception as err:
			self.log.error(err)
		return True


	async def sleep(self, m: Message, sec, delme=False):
		"""
		params: 
			1. message (update) :: incoming update
			2. sec :: time to sleep in seconds
			3. delme, default=False :: delete the message if it is True

		use: 
			this function deletes the message after sleeping for a given time,
			this function blocks the code

		ex: (async)
			await app.sleep(message, 10, delme=True)
		"""

		await asyncio.sleep(sec)
		if delme and m.from_user.is_self:
			m = await m.delete()
		return m


	async def delete(self, m: Message, sec: int = 0):
		"""
		params: 
			1. message (update) :: incoming update
			2. sec: int, default=0 :: time to sleep in seconds

		use: 
			this function deletes a message after given time period
			this function works without blocking the entire execution

		ex: (async)
			await app.delete(message, 10)
		"""

		if sec <= 600: # 10 min
			asyncio.create_task(self.sleep(m, sec=sec, delme=True))
			return True
		else:
			self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


	async def data(self, modules):
		"""
		params: 
			1. plug: str :: module name whose information is updated in app.CMD_HELP dict

		use: 
			use this function to get information about a module

		ex: (async)
			await app.data("admin")
		"""

		try:
			plugin_data = []
			plugin_data.clear()
	
			for x, y in zip(
				self.CMD_HELP.get(modules)[1].keys(), 
				self.CMD_HELP.get(modules)[1].values()
				):
				plugin_data.append(
					f"CMD: `{self.PREFIX}{x}`\nINFO: `{y}`\n\n"
					)
			return plugin_data
		except Exception as e:
			self.log.error(e)
			return None


	async def send_edit(
		self,
		m: Message, 
		text, 
		parse_mode="combined", 
		disable_web_page_preview=False,
		delme : int=0,
		text_type: list=[],
		mono=False,
		bold=False,
		italic=False,
		strike=False,
		underline=False,
		):
		"""
		params: 
			1. message (update) :: incoming update
			2. text: str :: text to be edited or sent instead of editing
			3. disable_web_page_preview: bool, default=False :: web page preview will be shown if True
			4. delme: int, default=0 :: sleeps for given time and then deletes the message
			5. mono: bool, default=False :: all text format will become mono
			6. bold: bool, default=False :: all text format will become bold
			7. italic: bool, default=False :: all text format will become italic
			8. underline: bool, defau=False :: all text format will become underlined

		use: 
			use this function to get realtime date of your location

		ex: (async)
			await app.send_edit(
				message, 
				"This text is sent or edited", 
				disable_web_page_preview=True,
				delme=5,
				mono=True
			)
		"""

		formats = [mono, bold, italic, strike, underline]

		format_dict = {
			mono : f"<code>{text}</code>", 
			bold : f"<b>{text}</b>",
			italic : f"<i>{text}</i>",
			strike : f"<s>{text}</s>",
			underline : f"<u>{text}</u>"
		}

		edited = False

		for x in formats:
			if x:
				m = await self.edit_text(
					m, 
					format_dict[x],
					disable_web_page_preview=disable_web_page_preview,
					parse_mode=parse_mode
				)
				edited = True
				break

		if not edited:
			m = await self.edit_text(
				m, 
				text, 
				disable_web_page_preview=disable_web_page_preview, 
				parse_mode=parse_mode
			)

		try:
			if delme > 0:
				asyncio.create_task(self.sleep(m, sec=delme, delme=True))

		except Exception as e:
			await self.error(m, e)
		return m


	async def private(self, m: Message):
		"""
		params: 
			1. message (update) :: incoming update

		use: 
			use this to tell that they can't use some commands in private

		ex: (async)
			await app.private(message)
		"""

		if m.chat.type == "private":
			await self.send_edit(
				m, 
				"Please use these commands in groups . . .",
				mono=True, 
				delme=True
			)
			return True
		return False


	def long(self, m: Message):
		"""
		params: 
			1. message (update) :: incoming update

		use: 
			this function returns the length of a list containing message splited on spaces

		ex: 
			if app.long(message) == 1:
				print("more arguments needed")
				return
		"""

		text_length = len(m.text.split())
		return text_length if bool(text_length) else None


	def textlen(self, m: Message):
		"""
		params: 
			1. message (update) :: incoming update

		use: 
			this function returns length of characters in message.text

		ex: 
			if app.textlen(message) > 4096:
				print("Text too long")
		"""

		return len([x for x in m.text or m.caption])


	async def create_file(self, m: Message, filename, text):
		"""
		params: 
			1. message (update) :: incoming update
			2. filename: str :: give a filename with some extension or without extension
			3. text: str :: contents which is going to be written in the file

		use: 
			use this function to create files with any type of extension (.txt, .py, .java, .html, etc),
			this function also sends the created file.

		ex: (async)
			await app.create_file(message, "sample.txt", "This file was created with app.create_file() method")
		"""

		try:
			name = filename
			content = text
			file = open(name, "w+")
			file.write(content)
			file.close()
			await self.send_document(
				m.chat.id,
				name,
				caption = f"**Uploaded By:** {self.UserMention()}"
				)
			if os.path.exists(name):
				os.remove(name)
			await m.delete()
		except Exception as e:
			await self.error(m, e)


	def rem_dual(self, one, two):
		"""
		params: 
			1. one: list :: list from that you want to remove duplicates
			2. two: list :: list that contains removable elements

		use: 
			use this function to remove duplicates from lists

		ex: 
			await app.rem_dual([1, 1, 1, 2, 3], [1])
		"""

		return list(set(one) - set(two))


	async def kick_user(self, chat_id, user_id, ban_time=30):
		"""
		params: 
			1. chat_id: int :: chat id of the chat where this method is used
			2. user_id: int :: user id of the user you want to kick from chat

		use: 
			use this function to kick a member from your chat

		ex: (async)
			await app.kick_user(chat_id, user_id)
		"""

		try:
			await self.ban_chat_member(chat_id, user_id, int(time.time()) + ban_time) 
			return True
		except Exception as e:
			await self.error(m, e)


	def is_str(self, element):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is string or not

		ex: 
			await app.is_str(data)
		"""

		return isinstance(element, str)


	def is_bool(self, element):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is boolean or not

		ex: 
			await app.is_bool(data)
		"""

		return isinstance(element, bool)


	def is_float(self, element):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is float or not

		ex: 
			await app.is_float(data)
		"""

		return isinstance(element, float)


	def is_int(self, element):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is integer or not

		ex: 
			await app.is_int(data)
		"""

		return isinstance(element, int)


	async def get_last_msg(self, m: Message, user_id, reverse=False):
		"""
		params: 
			1. message (update) :: incoming update
			2. chat_id: int :: chat id of group or user
			3. reverse: bool, default=False :: if reverse is True you'll get the oldest message in chat

		use: 
			use this function to get last message of the chat or user

		ex: (async)
			await app.get_last_msg(message, chat_id, reverse=True)
		"""

		return await self.get_history(user_id, limit=1, reverse=reverse)


	async def toggle_inline(self, m: Message):
		"""
		params: 
			1. message (update) :: incoming update

		use: 
			use this function to turn on | off inline mode of your bot

		ex: (async)
			await app.toggle_inline()
		"""

		try:
			botname = "BotFather"
			await self.send_edit(m, "Processing command . . .", mono=True)
			await self.send_message(botname, "/mybots") # BotFather (93372553) 
			await asyncio.sleep(1) # floodwaits
	
			data = await self.get_last_msg(m, botname)
			usernames = list(data[0].reply_markup.inline_keyboard)[0]
	
			unames = []
			unames.clear()
	
			for x in usernames:
				unames.append(x.text)
	
			await self.send_edit(m, "Choosing bot . . . ", mono=True)
	
			if self.bot.username in unames:
				await data[0].click(self.bot.username)
			else:
				return await self.send_edit(m, "Looks like you don't have a bot please, use your own bot . . .", mono=True, delme=True)
	
			data = await self.get_last_msg(m, botname)
	
			await self.send_edit(m, "Pressing Bot Settings . . . ", mono=True)
	
			await data[0].click("Bot Settings")
	
			data = await self.get_last_msg(m, botname)
	
			await self.send_edit(m, "checking whether inline mode is On or Off . . . ", mono=True)
	
			await data[0].click("Inline Mode")
	
			data = await self.get_last_msg(m, botname)
	
			# Turn on inline mode
			if "Turn on" in str(data[0]):
				await self.send_edit(m, "Turning Inline mode on . . . ", mono=True)
				await data[0].click("Turn on")
				await self.send_edit(m, "Inline mode is now turned On.", mono=True, delme=True)
			# Turn inline mode off
			elif "Turn inline mode off" in str(data[0]):
				await self.send_edit(m, "Turning Inline mode Off . . .", mono=True)
				await data[0].click("Turn inline mode off")
				await self.send_edit(m, "Inline mode is now turned Off.", mono=True, delme=True)
		except YouBlockedUser:
			await self.unblock_user(botname)
			await self.toggle_inline(m)
		except Exception as e:
			await self.error(m, e)


	def quote(self):
		"""
		params: 
			None

		use: 
			use this function to anime quotes

		ex: 
			await app.quote()
		"""

		results = requests.get("https://animechan.vercel.app/api/random").json()
		msg = f"❝ {results.get('quote')} ❞"
		msg += f" [ {results.get('anime')} ]\n\n"
		msg += f"- {results.get('character')}\n\n"
		return msg


	def ialive_pic(self):
		"""
		params: 
			None

		use: 
			use this function to get inline alive pic url

		ex: 
			await app.ialive_pic()
		"""

		return self.getdv("USER_PIC") or self.UserPic() or None


	def get_file_id(self, message):
		"""
		params: 
			1. message (update) :: incoming update 

		use: 
			use this function to get file_id of any media in telegram

		ex: 
			await app.get_file_id(message)
		"""

		media = ["photo", "video", "audio", "document", "sticker", "animation"]
	
		for x in media:
			if hasattr(message, x):
				if hasattr(message, "caption"):
					return [(message[x]).file_id, message.caption, x]
				else:
					return [(messsge[x]).file_id, None, x]
			elif hasattr(message, "text"):
				return [messsge.text, None, "text"]


	def clear_screen(self):
		"""
		params: 
			None

		use: 
			use this function to clear terminal screen

		ex:
			await app.clear_screen()
		"""

		subprocess.call("clear" if os.name == "posix" else "cls") 


	async def add_users(self, user_id: Union[int, List[int]], chat_id):
		"""
		params: 
			1. user_id: int :: list of telegram id of user
			2. chat_id :: chat id of a group or channel

		use: 
			use this function to add users in a group / channel

		ex: (async)
			await app.add_users(user_id, chat_id)
		"""

		try:
			done = await self.add_chat_members(chat_id, user_id)
			return True if done else False
		except Exception as e:
			self.log.error(e)


	async def user_exists(self, user_id: int, chat_id):
		"""
		params: 
			1. user_id: int :: id of a telegram user
			2. chat :: id of telegram chat

		use: 
			use this function to check whether a user exists in a group or not

		ex: (async)
			await app.user_exists(user_id, chat_id)
		"""

		async for x in self.iter_chat_members(chat_id):
			if x.user.id == user_id:
				return True
		return False


	async def add_logbot(self):
		"""
		params: 
			None

		use: 
			use this function to add your bot if he is not in the log chat

		ex: (async)
			await app.check_bot_in_log_chat()
		"""

		try:
			if self.bot:
				self.log.info("PROCESS: Checking presence of bot in log chat . . .\n")
				try:
					if await self.user_exists(self.bot.id, self.LOG_CHAT) is False:
						await self.add_users(self.bot.id, self.LOG_CHAT)
						self.log.info(f"COMPLETED: Added bot in log chat . . .\n")
					else:
						self.log.info(f"COMPLETED: Bot is already present in log chat . . .\n")
				except PeerIdInvalid:
					self.log.info("Peer id is invalid, Manually add bot to your log chat . . .\n")

			else:
				self.log.warning("Bot client is not available, please check (TOKEN, API_ID, API_HASH)")
		except Exception as e:
			await self.log.info(e)


	def uptime(self):
		"""
		params: 
			None

		use: 
			use this function to get ubot uptime

		ex: 
			await app.uptime()
		"""

		return self.GetReadableTime(time.time() - self.StartTime)


	def import_module(self, path, exclude=[], display_module=True):
		"""
		params: 
			1. path :: path of module directory
			2. exclude: list, default=[] :: exclude specific module installation
			3. display_module: bool, drfau=True :: whether to print module name after installation or not

		use: 
			use this function to install python modules 

		ex: 
			await app.import_module("./tronx/modules/", exclude=["admin"])
		"""

		bin = []
		bin.clear()

		if not os.path.exists(path):
			return self.log.info(f"No path found: {path}")

		plugins = []
		for x in os.listdir(path):
			if x.endswith(".py"):
				if not x in ["__pycache__",  "__init__.py"]:
					plugins.append(x.replace(".py", ""))

		py_path_raw = ".".join(path.split("/"))
		py_path = py_path_raw[0:len(py_path_raw)-1]

		count = 0
		for x in plugins:
			if not x in exclude:
				importlib.import_module(py_path + "." + x)
				count += 1
				bin.append(x)

		if display_module:
			data = sorted(bin)
			for x in data:
				self.log.info(x + " Loaded !")
		return count


	def db_status(self):
		"""
		params: 
			None

		use: 
			use this function to check if database is available or not

		ex: 
			await app.db_status()
		"""

		"Available" if self.DB_URI else "Unavailable"

