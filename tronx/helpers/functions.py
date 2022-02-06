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
		"""execute python codes"""
		exec(
			f"async def __aexec(self, m): "
			+ "".join(f"\n {l}" for l in code.split("\n"))
		)
		return await locals()["__aexec"](self, m)


	def showdate(self):
		"""your location's date"""
		today = pytz.timezone(self.TIME_ZONE)
		get_date = datetime.datetime.now(today)
		mydate = get_date.strftime("%d %b %Y")
		return mydate


	def showtime(self):
		"""your location's time"""
		today = pytz.timezone(self.TIME_ZONE)
		get_time = datetime.datetime.now(today)
		mytime = get_time.strftime("%r")
		return mytime


	async def edit_text(self, m: Message, text, disable_web_page_preview=False, parse_mode="combined"):
		"""this is a alias function for send_edit function"""
		try:
			if m.from_user and m.from_user.is_self:
				await m.edit(
					text, 
					parse_mode=parse_mode, 
					disable_web_page_preview=disable_web_page_preview,
				)
			elif m.from_user and not m.from_user.is_self: # for sudo users
				await self.send_message(
					m.chat.id,
					text,
					disable_web_page_preview=disable_web_page_preview,
					parse_mode=parse_mode
				)
		except Exception as e:
			self.log.info(e)


	async def error(self, m: Message, e, edit_error=False):
		"""Error tracing"""
		teks = f"**Traceback Report:**\n\n"
		teks += f"**Date:** {self.showdate()}\nTime: {self.showtime()}\n\n"
		teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
		teks += f"**Command:** {m.text}\n\n"
		teks += f"**Error:**\n\n"
		teks += f"**SHORT:** \n\n{e}\n\n"
		teks += f"**FULL:** \n\n{traceback.format_exc()}"

		try:
			if edit_error:
				if hasattr(e, "MESSAGE"):
					await self.send_edit(m, (e.MESSAGE.replace("(", "")).replace(")", ""))
				else:
					await self.send_edit(m, e.args)
		except Exception as err:
			print(err)

		try:
			await self.send_message(
				self.LOG_CHAT,
				teks
			)
		except PeerIdInvalid:
			print(teks)
		self.log.error("Please check your logs online.")


	async def sleep(self, m: Message, sec, delme=False):
		"""delete a message after some time"""
		await asyncio.sleep(sec)
		if delme and m.from_user.is_self:
			await m.delete()


	async def delete(self, m: Message, sec: int = 0):
		"""delete a message after some time using sleep func without blocking the code"""
		if sec <= 600: # 10 min
			asyncio.create_task(self.sleep(m, sec=sec, delme=True))
		else:
			self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


	async def data(self, plug):
		"""create help information page for each module"""
		try:
			plugin_data = []
			plugin_data.clear()
	
			for x, y in zip(
				self.CMD_HELP.get(plug)[1].keys(), 
				self.CMD_HELP.get(plug)[1].values()
				):
				plugin_data.append(
					f"CMD: `{self.PREFIX}{x}`\nINFO: `{y}`\n\n"
					)
			return plugin_data
		except Exception as e:
			self.log.info(e)
			return None


	async def send_edit(
		self,
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
		"""This function edits or exceptionally sends the message"""

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
				await self.edit_text(
					m, 
					format_dict[x],
					disable_web_page_preview=disable_web_page_preview,
					parse_mode=parse_mode
				)
				edited = True
				break

		if not edited:
			await self.edit_text(
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


	async def private(self, m : Message):
		"""stop user from using in private"""
		if m.chat.type == "private":
			await self.send_edit(
				m, 
				"Please use these commands in groups . . .",
				mono=True, 
				delme=True
			)
			return


	def long(self, m: Message):
		"""to check args, same as len(message.text.split())"""
		text = len(m.command)
		return text if bool(text) else none


	def textlen(self, m: Message):
		"""to check length of characters inside a message"""
		return len([x for x in m.text or m.caption])


	async def create_file(self, m: Message, filename, text):
		"""create a file with any type of extension"""
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
		"""remove multiples of same element from a list"""
		return list(set(one) - set(two))


	async def kick_user(self, chat_id, user_id):
		"""kick user from chat"""
		try:
			await self.kick_chat_member(chat_id, user_id)
		except Exception as e:
			print(e)


	def is_str(self, element):
		"""true if string else False"""
		return isinstance(element, str)


	def is_bool(self, element):
		"""true if boolean else False"""
		return isinstance(element, bool)


	def is_float(self, element):
		"""true if float else False"""
		return isinstance(element, float)


	def is_int(self, element):
		"""true if int else False"""
		return isinstance(element, int)


	async def get_last_msg(self, m: Message, user_id: int, reverse=False):
		"""get the first or last message of user/chat"""
		return await self.get_history(user_id, limit=1, reverse=reverse)


	async def toggle_inline(self, m: Message):
		"""turn on | off inline mode of your bot"""
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
		"""anime quotes for weebs"""
		results = requests.get("https://animechan.vercel.app/api/random").json()
		msg = f"❝ {results.get('quote')} ❞"
		msg += f" [ {results.get('anime')} ]\n\n"
		msg += f"- {results.get('character')}\n\n"
		return msg


	def ialive_pic(self):
		"""inline alive pic url"""
		pic_url = self.getdv("USER_PIC")
		data = pic_url if pic_url else self.UserPic()
		return data if data else None


	def get_file_id(self, message):
		"""get file id of supported telegram media"""
		media = ["photo", "video", "audio", "document", "sticker", "animation"]
	
		for x in media:
			if hasattr(message, x):
				if hasattr(message, "caption"):
					return [(message[x]).file_id, message.caption, x]
				else:
					return [(messsge[x]).file_id, None, x]
			elif hasattr(message, "text"):
				return [messsge.text, None, "text"]


	def clear():
		""" clear terminal prompt """
		subprocess.call("clear" if os.name == "posix" else "cls") 


	async def add_users(self, user_id: Union[int, List[int]], chat_id: str):
		""" add users in groups / channels """
		try:
			done = await self.add_chat_members(chat_id, user_id)
			return True if done else False
		except Exception as e:
			print(e)


	async def user_exists(self, user_id: int, chat_id: str):
		"""check whether a user exists in a group or not"""
		async for x in self.iter_chat_members(chat_id):
			if x.user.id == user_id:
				return True
		return False


	async def check_bot_in_log_chat(self):
		"""check pesence of bot (assistant) in log chat"""
		try:
			if bot:
				self.log.info("Checking presence of bot in log chat . . .\n")
				try:
					if await self.user_exists(self.bot.id, self.LOG_CHAT) is False:
						await self.add_user(self.LOG_CHAT, self.bot.id)
						self.log.info(f"Added bot in log chat . . .\n")
					else:
						self.log.info(f"Bot is already present in log chat . . .\n")
				except PeerIdInvalid:
					self.log.info("Peer id is invalid, Manually add bot to your log chat . . .\n")

			else:
				self.log.warning("Bot is not available, please check (TOKEN, API_ID, API_HASH)")
		except Exception as e:
			await self.log.info(e)


	def uptime(self):
		""" bot active time """
		return self.GetReadableTime(time.time() - self.StartTime)


	def import_module(self, path, exclude=[], display_module=True):
		"""include/exclude modules installation"""
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
		"""database is available or not"""
		"Available" if self.DB_URI else "Unavailable"
