import asyncio
import aiohttp

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"nekobin" : (
		"nekobin",
		{
		"bin [reply to text]" : "Paste Texts To Nekobin Site, You Can Easily Read The Texts Without Downloading The file." 
		}
		)
	}
)




@app.on_message(gen(["paste", "bin"], allow = ["sudo"]))
async def paster(_, m: Message):
	reply = m.reply_to_message

	if reply and reply.text or reply.caption:
		text = reply.text or reply.caption
	elif not reply and app.long(m) > 1:
		text = m.text.split(None, 1)[1]
	elif not reply and app.long(m) == 1:
		return await app.send_edit(m, "Please reply to a message or give some text after command.", text_type=["mono"], delme=4)

	try:
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"https://www.toptal.com/developers/hastebin/documents", data=text.encode("utf-8"), timeout=3
			) as response:
				key = (await response.json())["key"]
	except Exception as e:
		await app.error(m, e)
		return await app.send_edit(m, "Pasting failed, Try again later . . .", delme=4, text_type=["mono"])

	else:
		url = f"https://hastebin.com/raw/{key}"
		reply_text = f"**Hastebin** : [Click Here]({url})"
		delete = (True if app.long(m) > 1 and m.command[1] in ["d", "del"] and reply.from_user.is_self else False)
		if delete:
			await asyncio.gather(
				app.send_edit(
					m,  
					reply_text, 
					disable_web_page_preview=True
					),
				await reply.delete()
			)
		else:
			await app.send_edit(
				m,
				reply_text,
				disable_web_page_preview=True
			)
