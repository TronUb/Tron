from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"reddit" : (
		"reddit",
		{
		"r [query]" : "Get link of queries related reddit results."
		}
		)
	}
)




@app.on_message(gen(["r", "reddit"]))
async def reddit_link(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Please give some query to search on reddit ...", delme=2)

	elif app.long(m) > 1:
		try:
			text = m.text.split(None, 1)[1]
			await app.send_edit(
				m, 
				f"Reddit Link: [{text}](https://reddit.com/r/{text})",
				disable_web_page_preview=True,
				parse_mode="markdown"
			)
		except Exception as e:
			await app.error(m, e)
	elif len(m.text) > 4096:
		return await app.send_edit(m, "Too long query, only 4096 characters are allowed !", delme=2)

	else:
		await app.send_edit(m, "Try again later !", delme=2)
