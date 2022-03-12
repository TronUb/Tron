from pyrogram.errors import BotInvalid, BotInlineDisabled
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
		"ialive" : "Inline alive that contains your & your userbot status.",
		"qt" : "Get inline quotes with a inline 'more' button."
		}
		)
	}
)




@app.on_message(gen("alive", allow = ["sudo"]), group=0)
async def simple_alive(_, m: Message):
	try:
		m = await app.send_edit(m, ". . .", mono=True)

		alive_msg = f"\n"
		if app.UserBio():
			alive_msg += f"⦿ {app.UserBio()}\n\n"
		alive_msg += f"⟜ **Owner:** {app.UserMention()}\n"
		alive_msg += f"⟜ **Tron:** `{app.userbot_version}`\n"
		alive_msg += f"⟜ **Python:** `{app.python_version}`\n"
		alive_msg += f"⟜ **Pyrogram:** `{app.pyrogram_version}`\n"
		alive_msg += f"⟜ **Uptime:** {app.uptime()}\n\n"

		await m.delete()
		pic = app.UserPic()

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
			await app.send_edit(
				m, 
				alive_msg, 
				disable_web_page_preview=True,
				parse_mode="markdown",
				)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("ialive", allow = ["sudo"]), group=1)
async def inline_alive(_, m: Message):
	m = await app.send_edit(m, ". . .", mono=True)
	try:
		result = await app.get_inline_bot_results(app.bot.username, "#i2l8v3")
	except BotInlineDisabled:
		await app.send_edit(m, "Turning inline mode to on, wait . . .", mono=True)
		await app.toggle_inline(m)
		result = await app.get_inline_bot_results(app.bot.username, "#i2l8v3")

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




@app.on_message(gen(["qt"], allow = ["sudo"]), group=2)
async def inline_quote(_, m: Message):
	try:
		m = await app.send_edit(m,". . .", mono=True)
		try:
			result = await app.get_inline_bot_results(app.bot.username, "#q7o5e")
		except BotInlineDisabled:
			await app.send_edit(m, "Turning inline mode on, wait . . .", mono=True)
			await app.toggle_inline(m)
			result = await app.get_inline_bot_results(app.bot.username, "#q7o5e")

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

