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
from pyrogram.enums import ParseMode, ChatType





class RawFunctions(object):
	async def aexec(
		self, 
		code: str
		):
		"""
		params:
			1. code: str :: your written python code

		use:
			use this function to execute python codes

		ex: (async)
			await app.aexec("print('Hello, World !')")
		"""

		exec(
			f"async def __aexec(self, m): "
			+ "".join(f"\n {l}" for l in code.split("\n"))
		)
		return await locals()["__aexec"](self, self.m)


	def showdate(
		self
		):
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


	def showtime(
		self
		):
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


	async def error(
		self, 
		e, 
		edit_error: bool=True
		):
		"""
		params: 
			1. error :: occured error
			2. edit_error: bool, default=True :: edits | sends error message 

		usage:
			use this function at the end of try/except block

		ex: (async)
			try:
				await app.send_message(message.chat.id, "This is a test")
			except Exception as e:
				await app.error(e, edit_error=False) 
		"""

		teks = f"**Traceback Report:**\n\n"
		teks += f"**Date:** `{self.showdate()}`\n**Time:** `{self.showtime()}`\n\n"
		teks += f"`This can be a error in tronuserbot, if you want you can forward this to @tronuserbot_support.`\n\n" 
		teks += f"**Command:** `{self.m.text}`\n\n"
		teks += "`-`" * 30 + "\n\n"
		teks += f"**SHORT:** \n\n`{e}`\n\n"
		teks += f"**FULL:** \n\n`{traceback.format_exc()}`"

		try:
			if edit_error:
				if hasattr(e, "MESSAGE"):
					await self.send_edit(f"`{e.MESSAGE}`")
				else:
					await self.send_edit(e.args[0] if e.args else None)

			await self.send_message(self.LOG_CHAT, teks)
			print(e)

		except PeerIdInvalid:
			self.log.error(teks)
		except Exception as err:
			self.log.error(err)
		return True


	async def sleep(
		self, 
		sec: int=0, 
		delmsg=False
		):
		"""
		params: 
			1. sec :: time to sleep in seconds
			2. delme, default=False :: delete the message if it is True

		use: 
			this function deletes the message after sleeping for a given time,
			this function blocks the code

		ex: (async)
			await app.sleep(10, delmsg=True)
		"""
		msg = None
		await asyncio.sleep(sec)
		if delmsg and self.m.from_user.is_self:
			msg = await self.m.delete()
		return msg


	async def delete_message(
		self, 
		sec: int=0
		):
		"""
		params: 
			1. sec: int, default=0 :: time to sleep in seconds

		use: 
			this function deletes a message after given time period
			this function works without blocking the entire execution

		ex: (async)
			await app.delete(10)
		"""

		if sec <= 600: # 10 min
			asyncio.create_task(self.sleep(sec=sec, delmsg=True))
			return True
		else:
			self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


	async def data(
		self, 
		modules: str
		):
		"""
		params: 
			1. plug: str :: module name whose information is updated in app.CMD_HELP dict

		use: 
			use this function to get information about a module

		ex: (async)
			await app.data("admin")
		"""

		try:
			module_data = []
			module_data.clear()

			for x, y in zip(
				self.CMD_HELP.get(modules)[1].keys(), 
				self.CMD_HELP.get(modules)[1].values()
				):
				module_data.append(
					f"CMD: `{self.PREFIX}{x}`\nINFO: `{y}`\n\n"
					)
			return module_data
		except Exception as e:
			self.log.error(e)
			return None


	async def send_edit(
		self,
		text: str, 
		parse_mode=ParseMode.DEFAULT, 
		disable_web_page_preview=False,
		delme : int=0,
		text_type: list=[],
		disable_notification: bool=False,
		reply_to_message_id: int=0,
		schedule_date: int=0,
		protect_content: bool=False,
		reply_markup=None,
		entities=None
		):
		"""
		params: 
			1. text: str :: text to be edited or sent instead of editing
			2. disable_web_page_preview: bool, default=False :: web page preview will be shown if True
			3. delme: int, default=0 :: sleeps for given time and then deletes the message
			4. mono: bool, default=False :: all text format will become mono
			5. bold: bool, default=False :: all text format will become bold
			6. italic: bool, default=False :: all text format will become italic
			7. underline: bool, defau=False :: all text format will become underlined

		use: 
			use this function to edit or send a message if failed to edit message 

		ex: (async)
			await app.send_edit(
				"This text is sent or edited", 
				disable_web_page_preview=True,
				delme=5,
				mono=True
			)
		"""
		if self == self.bot:
			
			return
		msg = None

		if self.m.from_user.is_self:
			msg = await self.m.edit(
				text=self.FormatText(text, format=text_type),
				parse_mode=parse_mode,
				disable_web_page_preview=disable_web_page_preview,
				reply_markup=reply_markup,
				entities=entities
			)

		else:
			msg = await self.send_message(
				chat_id=self.m.chat.id, 
				text=self.FormatText(text, format=text_type),
				disable_web_page_preview=disable_web_page_preview, 
				parse_mode=parse_mode,
				reply_to_message_id=reply_to_message_id,
				schedule_date=schedule_date,
				protect_content=protect_content,
				reply_markup=reply_markup,
				entities=entities
			)

		try:
			if delme > 0:
				asyncio.create_task(self.sleep(sec=delme, delmsg=True))

		except Exception as err:
			await self.error(err)
		return msg


	async def check_private(
		self
		):
		"""
		params: 
			None

		use: 
			use this to tell that they can't use some commands in private

		ex: (async)
			await app.private(message)
		"""

		if self.m.chat.type == ChatType.PRIVATE:
			await self.send_edit(
				"Please use these commands in groups.",
				text_type=["mono"], 
				delme=4
			)
			return True
		return False


	def long(
		self
		):
		"""
		params: 
			None

		use: 
			this function returns the length of a list containing message splited on spaces

		ex: 
			if app.long() == 1:
				print("there is one word in message.text")
		"""

		text_length = len(self.m.text.split() or self.m.caption.split())
		return text_length if bool(text_length) is True else None


	def textlen(
		self
		):
		"""
		params: 
			None

		use: 
			this function returns length of characters in message.text

		ex: 
			if app.textlen() > 4096:
				print("Text is too long")
		"""

		return len([x for x in self.m.text or self.m.caption or None])


	async def create_file(
		self, 
		filename: str, 
		content: str,
		send: bool=True,
		caption: str=None
		):
		"""
		params: 
			1. filename: str :: give a filename with some extension or without extension
			2. text: str :: contents which is going to be written in the file

		use: 
			use this function to create files with any type of extension (.txt, .py, .java, .html, etc),
			this function also sends the created file.

		ex: (async)
			await app.create_file("sample.txt", "This file was created by app.create_file() method")
		"""

		try:
			path = f"./downloads/{filename}"
			file = open(path, "w+")
			file.write(content)
			file.close()
			if send:
				await self.send_document(
					self.m.chat.id,
					path,
					caption = caption if caption else f"**Uploaded By:** {self.UserMention()}"
				)
				if os.path.exists(path):
					os.remove(path)

			else:
				return path
		except Exception as e:
			await self.error(e)


	def rem_dual(
		self, 
		list1: list, 
		list2: list
		):
		"""
		params: 
			1. one: list :: list from that you want to remove duplicates
			2. two: list :: list that contains removable elements

		use: 
			use this function to remove duplicates from lists

		ex: 
			app.rem_dual([1, 1, 1, 2, 3], [1])
		"""

		return list(set(list1) - set(list2))


	async def kick_user(
		self, 
		chat_id: Union[str, int], 
		user_id: Union[str, int], 
		ban_time: int=30
		):
		"""
		params: 
			1. chat_id: int :: chat id of the chat where this method is used
			2. user_id: int :: user id of the user you want to kick from chat

		use: 
			use this function to kick a member from your chat

		ex: (async)
			await app.kick_user(chat_id, user_id, ban_time=120)
		"""

		try:
			return await self.ban_chat_member(chat_id, user_id, int(time.time()) + ban_time) 
		except Exception as e:
			await self.error(e)


	def is_str(
		self, 
		element
		):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is string or not

		ex: 
			app.is_str(data)
		"""

		return isinstance(element, str)


	def is_bool(
		self, 
		element
		):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is boolean or not

		ex: 
			app.is_bool(data)
		"""

		return isinstance(element, bool)


	def is_float(
		self, 
		element
		):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is float or not

		ex: 
			app.is_float(data)
		"""

		return isinstance(element, float)


	def is_int(
		self, 
		element
		):
		"""
		params: 
			1. element: [str, bool, int, float] :: anytype of data

		use: 
			use this function to check if the element is integer or not

		ex: 
			app.is_int(data)
		"""

		return isinstance(element, int)


	async def get_last_msg(
		self, 
		chat_id, 
		reverse: bool=False
		):
		"""
		params: 
			1. chat_id: int :: chat id of group or user
			2. reverse: bool, default=False :: if reverse is True you'll get the oldest message in chat

		use: 
			use this function to get last message of the chat or user

		ex: (async)
			await app.get_last_msg(chat_id, reverse=True)
		"""

		return await self.get_chat_history(chat_id, limit=1, reverse=reverse)


	async def toggle_inline(
		self, 
		):
		"""
		params: 
			None

		use: 
			use this function to turn on | off inline mode of your bot

		ex: (async)
			await app.toggle_inline()
		"""

		try:
			botname = "BotFather"
			await self.send_edit("Processing command . . .", text_type=["mono"])
			await self.send_message(botname, "/mybots") # BotFather (93372553) 
			await asyncio.sleep(0.50) # floodwaits

			data = await self.get_last_msg(botname)
			usernames = list(data[0].reply_markup.inline_keyboard)[0]

			unames = []
			unames.clear()

			for x in usernames:
				unames.append(x.text)

			await self.send_edit("Choosing bot . . . ", text_type=["mono"])

			if self.bot.username in unames:
				await data[0].click(self.bot.username)
			else:
				return await self.send_edit("Looks like you don't have a bot please, use your own bot.", text_type=["mono"], delme=4)

			data = await self.get_last_msg(botname)

			await self.send_edit("Pressing Bot Settings . . . ", text_type=["mono"])

			await data[0].click("Bot Settings")

			data = await self.get_last_msg(botname)

			await self.send_edit("checking whether inline mode is On or Off . . . ", text_type=["mono"])

			await data[0].click("Inline Mode")

			data = await self.get_last_msg(botname)

			# Turn on inline mode
			if "Turn on" in str(data[0]):
				await self.send_edit("Turning Inline mode on . . . ", text_type=["mono"])
				await data[0].click("Turn on")
				await self.send_edit("Inline mode is now turned On.", text_type=["mono"], delme=4)
			# Turn inline mode off
			elif "Turn inline mode off" in str(data[0]):
				await self.send_edit("Turning Inline mode Off . . .", text_type=["mono"])
				await data[0].click("Turn inline mode off")
				await self.send_edit("Inline mode is now turned Off.", text_type=["mono"], delme=4)
		except YouBlockedUser:
			await self.unblock_user(botname) # unblock & continue
			await self.toggle_inline() # keep process going
		except Exception as err:
			await self.error(err)


	def quote(
		self
		):
		"""
		params: 
			None

		use: 
			use this function to anime quotes

		ex: 
			app.quote()
		"""

		results = requests.get("https://animechan.vercel.app/api/random").json()
		msg = f"❝ {results.get('quote')} ❞"
		msg += f" [ {results.get('anime')} ]\n\n"
		msg += f"- {results.get('character')}\n\n"
		return msg


	def ialive_pic(
		self
		):
		"""
		params: 
			None

		use: 
			use this function to get inline alive pic url

		ex: 
			app.ialive_pic()
		"""

		return self.getdv("USER_PIC") or self.UserPic() or None


	def get_file_id(
		self, 
		message: Message
		):
		"""
		params: 
			1. message (update) :: incoming update 

		use: 
			use this function to get file_id of any media in telegram

		ex: 
			app.get_file_id(message)
		"""

		media = ["photo", "video", "audio", "document", "sticker", "animation"]
	
		for x in media:
			if message and message[x]:
				if message["caption"]:
					return {"data":(message[x]).file_id, "caption":message.caption, "type":x}
				else:
					return {"data":(message[x]).file_id, "caption":None, "type":x}
			elif message["text"]:
				return {"data":message.text, "caption":None, "type":"text"}
		return {"data":None, "caption":None, "type":None}


	def clear_screen(
		self
		):
		"""
		params: 
			None

		use: 
			use this function to clear terminal screen

		ex:
			app.clear_screen()
		"""

		subprocess.call("clear" if os.name == "posix" else "cls") 


	async def add_users(
		self, 
		user_id: Union[int, str, List[int], List[str]], 
		chat_id: Union[int, str]
		):
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


	async def user_exists(
		self, 
		user_id: Union[int, str],
		chat_id: Union[int, str]
		):
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


	async def add_logbot(
		self
		):
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
		except Exception as err:
			await self.log.info(err)


	def uptime(
		self
		):
		"""
		params: 
			None

		use: 
			use this function to get ubot uptime

		ex: 
			app.uptime()
		"""

		return self.GetReadableTime(time.time() - self.StartTime)


	def import_module(
		self, 
		path: str, 
		exclude: list=[], 
		display_module: bool=True
		):
		"""
		params: 
			1. path :: path of module directory
			2. exclude: list, default=[] :: exclude specific module installation
			3. display_module: bool, drfau=True :: whether to print module name after installation or not

		use: 
			use this function to install python modules 

		ex: 
			app.import_module("./tronx/modules/", exclude=["admin"])
		"""

		listbin = []
		listbin.clear()

		if not os.path.exists(path):
			return self.log.info(f"No path found: {path}")

		modules = []
		modules.clear()

		for x in os.listdir(path):
			if x.endswith(".py"):
				if not x in ["__pycache__",  "__init__.py"]:
					modules.append(x.replace(".py", ""))

		py_path_raw = ".".join(path.split("/"))
		py_path = py_path_raw[0:len(py_path_raw)-1]

		count = 0
		for x in modules:
			if not x in exclude:
				importlib.import_module(py_path + "." + x)
				count += 1
				listbin.append(x)

		if display_module:
			data = sorted(listbin)
			for x in data:
				print(x + " Loaded !")
		return count


	def db_status(
		self
		):
		"""
		params: 
			None

		use: 
			use this function to check if database is available or not

		ex: 
			app.db_status()
		"""

		"Available" if self.DB_URI else "Unavailable"
  