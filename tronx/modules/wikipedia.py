import time
import wikipedia

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
)




CMD_HELP.update(
	{"wikipedia" : (
		"wikipedia",
		{
		"wiki [ query ]" : "Get info about anything on Wikipedia."
		}
		)
	}
)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




@app.on_message(gen("wiki"))
async def wikipedia_search(app, m:Message):
	if len(m.command) < 2:
		await send_edit(
			m, 
			"Need some query to search on wikipedia, try again."
			)
	elif len(m.command) > 1:
		try:
			await send_edit(
				m, 
				"`Searching ...`")
			text = m.text.split(None, 1)[1]
			result = wikipedia.summary(text)
			if result and len(result) < 4096:
				await send_edit(
					m, 
					f"**Results for:** `{m.text.split(None, 1)[1]}`\n\n{result}"
					)
			else:
				await send_edit(
					m, 
					"No results found !"
					)
				time.sleep(1)
				await m.delete()
		except Exception as e:
			await app.resolve_peer(
				Config.LOG_CHAT
				)
			await error(m, e)
			await send_edit(
				m, 
				"Check your log chat for error report !"
				)
	else:
		await send(
			m, 
			"Something went wrong !"
			)