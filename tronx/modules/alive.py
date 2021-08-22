import os

from sys import version_info

from pyrogram.errors import BotInvalid
from pyrogram import filters
from pyrogram import filters,  __version__ as __pyro_version__
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
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
	gen,
	send_edit,
	BOT_USERNAME,
)




CMD_HELP.update(
	{
		"alive":f"""
**PLUGIN:** `alive`\n\n
**COMMAND:** `{PREFIX}alive` \n**USAGE:** Normal alive, in which you will get userbot status without inline buttons.\n\n
**COMMAND:** `{PREFIX}ialive` \n**USAGE:** Inline alive that contains your & your userbot status.\n\n
"""
	}
)




__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"



# commands
@app.on_message(gen("alive"))
async def alive(app, m: Message):
	await alive(m)




@app.on_message(gen(["ialive", "inline"]))
async def inline_alive(app, m: Message):
	await ialive(m)




@app.on_message(gen(["qt"]))
async def inline_alive(app, m):
	await quote(m)




# functions
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

