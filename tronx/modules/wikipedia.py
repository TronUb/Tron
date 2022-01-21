import time
import wikipediaapi

from pyrogram import filters
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
	error,
	send_edit,
	long,
)




app.CMD_HELP.update(
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
async def wikipedia_search(_, m: Message):
	if long(m) == 1:
		await send_edit(m, "Give me some query to search on wikipedia . . .", mono=True, delme=True)

	elif long(m) > 1 and long(m) < 4096:
		try:
			obj = wikipediaapi.Wikipedia("en")
			text = m.text.split(None, 1)[1]
			result = obj.page(text)
			await send_edit(m, f"Searching for: __{text}__ . . .", mono=True)
			if result:
				giveresult = result.summary
				if len(giveresult) <= 4096:
					await send_edit(m, f"**Results for:** `{text}`\n\n```{giveresult}```")
				else:
					await send_edit(m, f"**Results for:** `{text}`\n\n```{giveresult[:4095]}```")
			else:
				await send_edit(m, "No results found !", delme=2, mono=True)
		except Exception as e:
			await error(m, e)
	else:
		await send(m, "Something went wrong !", mono=True, delme=3)
