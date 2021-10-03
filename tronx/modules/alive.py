import time

from sys import version_info

from pyrogram.errors import BotInvalid
from pyrogram import __version__ as __pyro_version__
from pyrogram.types import Message

from tronx import (
	app,
	CMD_HELP,
	version, 
	uptime,
	Config,
	__python_version__,
	)

from tronx.helpers import (
	gen,
	error,
	mymention,
	send_edit,
	BOT_USERNAME,
)

from tronx.database.postgres import dv_sql as db




CMD_HELP.update(
	{"alive" : (
		"alive",
		{
		"alive" : "Normal alive, in which you will get userbot status without inline buttons.",
		"ialive" : "Inline alive that contains your & your userbot status."
		}
		)
	}
)




@app.on_message(gen("alive"))
async def alive(app, m: Message):
	try:
		await send_edit(m, "...")

		if db.getdv("USER_BIO"):
			BIO = db.getdv("USER_BIO")
		elif Config.USER_BIO:
			BIO = Config.USER_BIO

		alive_msg = f"⦿ {BIO}\n\n"
		alive_msg += f"⟜ **Owner:** {mymention()}\n"
		alive_msg += f"⟜ **Tron:** `{version}`\n"
		alive_msg += f"⟜ **Python:** `{__python_version__}`\n"
		alive_msg += f"⟜ **Pyrogram:** `{__pyro_version__}`\n"
		alive_msg += f"⟜ **Uptime:** {uptime()}\n\n"

		await m.delete()
		if db.getdv("USER_PIC"):
			pic = db.getdv("USER_PIC")
		elif Config.USER_PIC:
			pic = Config.USER_PIC

		if (pic) and (pic.endswith(".mp4" or ".mkv" or ".gif")):
			await app.send_video(
				m.chat.id, 
				pic, 
				caption=alive_msg, 
				parse_mode="markdown"
				)
		elif (pic) and (pic.endswith(".jpg" or ".jpeg" or ".png")):
			await app.send_photo(
				m.chat.id, 
				pic, 
				caption=alive_msg, 
				parse_mode="markdown"
				)
		elif not pic:
			await app.send_message(
				m.chat.id, 
				alive_msg, 
				disable_web_page_preview=True,
				parse_mode="markdown",
				)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["ialive", "inline"]))
async def inline_alive(app, m: Message):
	await send_edit(m, "`...`")
	try:
		result = await app.get_inline_bot_results(
			BOT_USERNAME, 
			"#i2l8v3"
		)
	except BotInvalid:
		await send_edit(
			m, 
			"The bot can't be used in inline mode",
			delme=2
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
			"Something went wrong, please try again later . . .",
			delme=2
		)




@app.on_message(gen(["qt"]))
async def inline_alive(_, m: Message):
	try:
		await send_edit(m,"...")
		try:
			result = await app.get_inline_bot_results(BOT_USERNAME, "#q7o5e")
		except BotInvalid:
			await send_edit(m,"This bot can't be used in inline mode.", delme=2)
			return
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
				await error(m, e)
		else:
			await send_edit(
				m, 
				"Failed to get inline alive results !",
				delme=2
				)
	except Exception as e:
		await error(m, e)

