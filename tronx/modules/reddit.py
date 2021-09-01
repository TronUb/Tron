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
	{"reddit" : (
		"reddit",
		{
		"r [query]" : "Get link of queries related reddit results."
		}
		)
	}
)




@app.on_message(gen(["r", "reddit"]))
async def subreddit_link(_, m: Message):
	if len(m.command) < 2:
		await send_edit(
			m, 
			"Please give some query to search on reddit ..."
			)
		return
	elif len(m.command) > 1:
		try:
			text = m.text.split(None, 1)[1]
			await m.edit(
				f"Reddit Link: [{text}](https://reddit.com/r/{text})",
				disable_web_page_preview=True,
				parse_mode="markdown"
			)
		except Exception as e:
			await error(m, e)
	elif len(m.text) > 4096:
		await send_edit(
			m, 
			"Too long query, only 4096 charactes allowed !"
			)
		return
	else:
		await send_edit(
			m, 
			"Something went wrong !"
			)