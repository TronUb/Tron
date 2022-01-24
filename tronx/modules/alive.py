from pyrogram.errors import BotInvalid
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
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
async def simple_alive(_, m: Message):
	try:
		await app.send_edit(m, ". . .", mono=True)

		if app.getdv("USER_BIO"):
			BIO = app.getdv("USER_BIO")
		elif app.USER_BIO:
			BIO = app.USER_BIO
		else:
			BIO = False

		alive_msg = f"\n"
		if BIO:
			alive_msg += f"⦿ {BIO}\n\n"
		alive_msg += f"⟜ **Owner:** {app.mymention()}\n"
		alive_msg += f"⟜ **Tron:** `{app.userbot_version}`\n"
		alive_msg += f"⟜ **Python:** `{app.python_version}`\n"
		alive_msg += f"⟜ **Pyrogram:** `{app.pyrogram_version}`\n"
		alive_msg += f"⟜ **Uptime:** {app.uptime()}\n\n"

		await m.delete()
		if app.getdv("USER_PIC"):
			pic = app.getdv("USER_PIC")
		elif app.USER_PIC:
			pic = app.USER_PIC

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
		await app.error(m, e)




@app.on_message(gen("ialive"))
async def inline_alive(_, m: Message):
	await app.send_edit(m, ". . .", mono=True)
	try:
		result = await app.get_inline_bot_results(app.bot.username, "#i2l8v3")
	except BotInvalid:
		return await app.send_edit(m, "The bot can't be used in inline mode", delme=2)

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
		await app.send_edit(m, "Something went wrong, please try again later . . .", delme=2)




@app.on_message(gen(["qt"]))
async def inline_quote(_, m: Message):
	try:
		await app.send_edit(m,". . .")
		try:
			result = await app.get_inline_bot_results(BOT_USERNAME, "#q7o5e")
		except BotInvalid:
			return await app.send_edit(m,"This bot can't be used in inline mode.", delme=2)

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
			await app.send_edit(m, "Please try again later !", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)

