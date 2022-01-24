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




@app.on_message(gen(["neko", "bin"]))
async def paster(_, m: Message):
	reply = m.reply_to_message
	await app.send_edit(m, "`Pasting to nekobin ...`")

	if reply:
		text = reply.text
	elif not reply and app.long(m) > 1:
		text = m.text.split(None, 1)[1]
	else:
		return await app.send_edit(m, "Please reply to a message or give some text after command.", delme=2)

	try:
		async with aiohttp.ClientSession() as session:
			async with session.post(
				"https://nekobin.com/api/documents", json={"content": text}, timeout=3
			) as response:
				key = (await response.json())["result"]["key"]
	except Exception as e:
		return await app.send_edit(m, "Pasting failed, Try again . . .", delme=2, mono=True)
		print(e)

	else:
		url = f"https://nekobin.com/{key}"
		reply_text = f"**Nekobin** : [Here]({url})"
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
