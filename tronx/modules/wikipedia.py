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
	long,
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
	if long(m) == 1:
		await send_edit(m, "Need some query to search on wikipedia, try again.", mono=True)

	elif long(m) > 1 and long(m) < 4096:
		try:
			await send_edit(m, "Searching . . .", mono=True)
			text = m.text.split(None, 1)[1]
			result = wikipedia.summary(text)
			if result and len(result) < 4096:
				if result.endswith("Try another id!"):
					return await send_edit(m, "No results found !", mono=True)
				await send_edit(m, f"**Results for:** ```{text}```\n\n{result}")
			else:
				await send_edit(m, "No results found !", delme=2, mono=True)
		except Exception as e:
			await error(m, e)
	else:
		await send(m, "Something went wrong !", mono=True)