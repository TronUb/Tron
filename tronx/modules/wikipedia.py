import time
import wikipediaapi

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
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




@app.on_message(gen("wiki", allow = ["sudo", "channel"]))
async def wikipedia_search(_, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Give me some query to search on wikipedia . . .", text_type=["mono"], delme=True)

	elif app.long(m) > 1 and app.long(m) < 4096:
		try:
			obj = wikipediaapi.Wikipedia("en")
			text = m.text.split(None, 1)[1]
			result = obj.page(text)
			await app.send_edit(m, f"Searching for: __{text}__ . . .", text_type=["mono"])
			if result:
				giveresult = result.summary
				if len(giveresult) <= 4096:
					await app.send_edit(m, f"**Results for:** `{text}`\n\n```{giveresult}```")
				else:
					await app.send_edit(m, f"**Results for:** `{text}`\n\n```{giveresult[:4095]}```")
			else:
				await app.send_edit(m, "No results found !", delme=2, text_type=["mono"])
		except Exception as e:
			await app.error(m, e)
	else:
		await app.send(m, "Something went wrong !", text_type=["mono"], delme=3)
