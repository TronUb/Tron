import os
import pytz
import datetime
import asyncio
import traceback
import requests

from pyrogram.types import Message
from pyrogram.errors import YouBlockedUser, MessageIdInvalid, PeerIdInvalid

from tronx.database.postgres import dv_sql as dv




class Functions(object):
	async def aexec(self, m, code):
		exec(
			f"async def __aexec(self, m): "
			+ "".join(f"\n {l}" for l in code.split("\n"))
		)
		return await locals()["__aexec"](self, m)


	def showdate(self):
		"""Your location's date"""
		today = pytz.timezone(self.TIME_ZONE)
		get_date = datetime.datetime.now(today)
		mydate = get_date.strftime("%d %b %Y")
		return mydate


	def showtime(self):
		"""Your location's time"""
		today = pytz.timezone(self.TIME_ZONE)
		get_time = datetime.datetime.now(today)
		mytime = get_time.strftime("%r")
		return mytime


	async def edit_text(self, m: Message, text, disable_web_page_preview=False, parse_mode="combined"):
		"""edit or send that message"""
		try:
			await m.edit(
				text, 
				parse_mode=parse_mode, 
				disable_web_page_preview=disable_web_page_preview,
			)
		except MessageIdInvalid:
			await self.send_message(
				m.chat.id,
				text,
				disable_web_page_preview=disable_web_page_preview,
				parse_mode=parse_mode
			)


	async def send_msg(self, m: Message, text):
		"""Send message"""
		try:
			await self.send_message(
				m.chat.id,
				text
			)
		except Exception as e:
			await error(m, e)


	async def error(self, m: Message, e):
		"""Error tracing"""
		teks = f"Traceback Report:\n\n"
		teks += f"Date: {self.showdate()}\nTime: {self.showtime()}\n\n"
		teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
		teks += f"Command: {m.text}\n\n"
		teks += f"Error:\n\n"
		teks += f"**SHORT:** \n\n{e}\n\n"
		teks += f"**FULL:** \n\n{traceback.format_exc()}"
		try:
			await self.send_message(
				self.LOG_CHAT,
				teks
			)
		except PeerIdInvalid:
			print(teks)
		self.log.error("Please check your logs online.")


	async def sleep(self, m: Message, sec, del_msg=False):
		"""Delete a message after some time"""
		await asyncio.sleep(sec)
		if del_msg and m.from_user.is_self:
			await m.delete()


	async def delete(self, m: Message, sec: int = 0):
		"""Delete a message after some time using sleep func"""
		if sec <= 600: # 10 min
			asyncio.create_task(self.sleep(m, sec=sec, del_msg=True))
		else:
			self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


	async def data(self, plug):
		"""Create help information page for each module"""
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
			print(e)
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
		"""This function edits or sends the message"""

		formats = [mono, bold, italic, strike, underline]

		format_dict = {
			"mono" : f"<code>{text}</code>", 
			"bold" : f"<b>{text}</b>",
			"italic" : f"<i>{text}</i>",
			"strike" : f"<s>{text}</s>",
			"underline" : f"<u>{text}</u>"
		}

		edited = False

		for x in formats:
			if x:
				await self.edit_text(
					m, 
					format_dict[x],
					disable_wab_page_preview=disable_wab_page_preview,
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
				asyncio.create_task(self.sleep(m, sec=delme, del_msg=True))

		except Exception as e:
			await self.error(m, e)


	async def private(self, m : Message):
		"""Stop user from using in private"""
		if m.chat.type == "private":
			await self.send_edit(
				m, 
				"Please use these commands in groups . . .",
				mono=True, 
				delme=True
			)


	def long(self, m: Message):
		"""to check args, same as len(message.text.split())"""
		text = len(m.command)
		return text if text else None


	async def create_file(self, m: Message, filename, text):
		"""Create a file with anytype of extension"""
		try:
			name = filename
			content = text
			file = open(name, "w+")
			file.write(content)
			file.close()
			await self.send_document(
				m.chat.id,
				name,
				caption = f"**Uploaded By:** {self.mymention()}"
				)
			os.remove(name)
			await m.delete()
		except Exception as e:
			await error(m, e)


	def rem_dual(self, one, two):
		"""remove multiples of same element from a list"""
		return list(set(one) - set(two))
	
	
	async def kick(self, chat_id, user_id):
		"""kick user from chat"""
		try:
			await self.kick_chat_member(
				chat_id,
				user_id
				)
		except Exception as e:
			print(e)
	
	
	def is_str(self, element):
		"""True if string else False"""
		return isinstance(element, str)
	
	
	def is_bool(self, element):
		"""True if boolean else False"""
		return isinstance(element, bool)
	
	
	def is_float(self, element):
		"""True if float else False"""
		return isinstance(element, float)
	
	
	def is_int(self, element):
		"""True if int else False"""
		return isinstance(element, int)
	
	
	async def textlen(self, m: Message, num: int = 1):
		"""auto check and warn if not suffix with command"""
		try:
			cmd = True if len(m.command) > num else False
			text = True if len(m.text) > 1 and len(m.text) <= 4096 else False
			if cmd is False:
				await self.send_edit(m, "Please give me some suffix . . .", mono=True, delme=3)
			elif text is False:
				await self.send_edit(m, "Only 4096 characters are allowed !", mono=True, delme=3)
			else: 
				return False
		except Exception as e:
			print(e)
			await error(m, e)
	
	
	async def get_last_msg(self, m: Message, user_id: int, reverse=False):
		"""Get the first or last message of user chat"""
		if reverse:
			data = await self.get_history(user_id, limit=1, reverse=True)
		else:
			data = await self.get_history(user_id, limit=1)
		return data
	
	
	async def toggle_inline(self, m: Message):
		"""Turn on | off inline mode of your bot"""
		try:
			await self.send_edit(m, "Processing command . . .", mono=True)
			await self.send_message("BotFather", "/mybots") # BotFather (93372553) 
			await asyncio.sleep(1) # floodwaits
	
			data = await self.get_last_msg(m)
			usernames = list(data[0].reply_markup.inline_keyboard)[0]
	
			unames = []
			unames.clear()
	
			for x in usernames:
				unames.append(x.text)
	
			await self.send_edit(m, "Choosing bot . . . ", mono=True)
	
			if self.Bot_Username() in unames:
				await data[0].click(self.Bot_Username())
			else:
				return await self.send_edit(m, "Looks like you don't have a bot please, use your own bot . . .", mono=True, delme=True)
	
			data = await self.get_last_msg(m)
	
			await self.send_edit(m, "Pressing Bot Settings . . . ", mono=True)
	
			await data[0].click("Bot Settings")
	
			data = await self.get_last_msg(m)
	
			await self.send_edit(m, "checking whether inline mode is On or Off . . . ", mono=True)
	
			await data[0].click("Inline Mode")
	
			data = await self.get_last_msg(m)
	
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
			await self.unblock_user("BotFather")
			await self.toggle_inline(m)
		except Exception as e:
			await error(m, e)
	
	
	def quote(self):
		"""anime quotes for weebs"""
		results = requests.get("https://animechan.vercel.app/api/random").json()
		msg = f"❝ {results.get('quote')} ❞"
		msg += f" [ {results.get('anime')} ]\n\n"
		msg += f"- {results.get('character')}\n\n"
		return msg
	
	
	def ialive_pic(self):
		"""inline alive pic url"""
		pic_url = dv.getdv("USER_PIC")
		data = pic_url if pic_url else self.UserPic()
		return data if data else None
	
	
	
	def get_file_id(self, message):
		media = ["video", "audio", "document", "sticker", "animation"]
	
		for x in media:
			if hasattr(message, x):
				if hasattr(message, "caption"):
					return [message[x].file_id, message.caption, "media"]
				else:
					return [messsge[x].file_id, None, "media"]
			elif hasattr(message, "text"):
				return [messsge.text, None, "text"]
