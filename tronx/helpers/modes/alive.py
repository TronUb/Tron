import os

from sys import version_info

from pyrogram.errors import BotInvalid
from pyrogram import __version__ as __pyro_version__
from pyrogram.types import Message

from tronx import (
	version, 
	USER_NAME, 
	USER_ID,
	OWNER_ID,
	uptime,
	Config,
	PREFIX
	)

from tronx.helpers import (
	error,
	mymention,
	send_edit,
	BOT_USERNAME,
)




__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"




# normal alive
async def alive(m: Message):
	try:
		await send_edit(
			m,
			"..."
			)
		alive_msg = f"⦿ {Config.USER_BIO}\n\n"
		alive_msg += f"⟜ **Owner:** {mymention()}\n"
		alive_msg += f"⟜ **Tron:** `{version}`\n"
		alive_msg += f"⟜ **Python:** `{__python_version__}`\n"
		alive_msg += f"⟜ **Pyrogram:** `{__pyro_version__}`\n"
		alive_msg += f"⟜ **Uptime:** {uptime()}\n\n"
		await m.delete()
		if (Config.USER_PIC) and (Config.USER_PIC.endswith(".mp4" or ".mkv")):
			await app.send_video(
				m.chat.id, 
				Config.USER_PIC, 
				caption=alive_msg, 
				parse_mode="markdown"
				)
		elif (Config.USER_PIC) and (Config.USER_PIC.endswith(".jpg" or ".jpeg" or ".png")):
			await app.send_photo(
				m.chat.id, 
				Config.USER_PIC, 
				caption=alive_msg, 
				parse_mode="markdown"
				)
		elif not Config.USER_PIC:
			await app.send_message(
				m.chat.id, 
				alive_msg, 
				disable_web_page_preview=True,
				parse_mode="markdown",
				)
	except Exception as e:
		await error(m, e)




# inline alive
async def ialive(m: Message):
	await send_edit(m, "`...`")
	try:
		result = await app.get_inline_bot_results(
			BOT_USERNAME, 
			"#i2l8v3"
		)
	except BotInvalid:
		await send_edit(
			"The bot can't be used in inline mode"
		)
		return
	if result:
		await app.send_inline_bot_result(
			m.chat.id, 
			query_id=result.query_id, 
			result_id=result.results[0].id, 
			disable_notification=True, 
			hide_via=True
		)
		await m.delete()
	else:
		await send_edit(
			m, 
			"Failed to get inline alive results !",
		)




# inline quotes
async def quote(m: Message):
	try:
		await send_edit(
			m,
			"..."
			)
		try:
			result = await app.get_inline_bot_results(BOT_USERNAME, "#q7o5e")
		except BotInvalid:
			await send_edit(
				m,
				"This bot can't be used in inline mode."
				)
		if result:
			try:
				await app.send_inline_bot_result(
					m.chat.id, 
					query_id=result.query_id, 
					result_id=result.results[0].id, 
					disable_notification=True, 
					hide_via=True
					)
				await m.delete()
			except Exception as e:
				await error(e)
		else:
			await send_edit(
				m, 
				"Failed to get inline alive results !"
				)
	except Exception as e:
		await error(m, e)

