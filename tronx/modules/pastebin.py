import asyncio
import aiohttp

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
)




CMD_HELP.update(
	{
		"nekobin": f"""
**PLUGIN:** `nekobin`\n\n
**COMMAND:** `{PREFIX}neko [ reply to text ]` or `{PREFIX}bin [ reply to text ]` \n**USAGE:** Paste Texts To Nekobin Site, You Can Easily Read The Texts Without Downloading The file.\n
"""
	}
)




@app.on_message(gen(["neko", "bin"]))
async def paster(_, m: Message):
	await send_edit(
		m, 
		"`Pasting to nekobin ...`"
		)
	if m.reply_to_message:
		text = m.reply_to_message.text
	elif not m.reply_to_message and (len(m.text)) > 1:
		text = m.text.split(None, 1)[1]
	else:
		await send_edit(
			m, 
			"Please reply to a message or give some text after command."
			)
		return
	try:
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"https://nekobin.com/api/documents", json={"content": text}, timeout=3
			) as response:
				key = (await response.json())["result"]["key"]
	except Exception:
		await send_edit(
			m, 
			"`Pasting failed, Try again ...`"
			)
		await asyncio.sleep(1)
		await m.delete()
	else:
		url = f"https://nekobin.com/{key}"
		reply_text = f"**Nekobin** : [Here]({url})"
		delete = (
			True
			if len(m.command) > 1
			and m.command[1] in ["d", "del"]
			and m.reply_to_message.from_user.is_self
			else False
		)
		if delete:
			await asyncio.gather(
				app.send_message(
					m.chat.id, 
					reply_text, 
					disable_web_page_preview=True
				),
				m.reply_to_message.delete(),
				m.delete(),
			)
		else:
			await send_edit(
				m,
				reply_text,
				disable_web_page_preview=True
			)