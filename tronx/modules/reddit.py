import os
import json
import random
import requests
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
async def reddit_image(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Please give some query to search on reddit ...", delme=2)

	elif app.long(m) > 1:
		try:
			text = m.text.split(None, 1)[1]
			url = f"https://old.reddit.com/r/{text}.json"

			headers = {
				"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
			}
			data = requests.get(url, headers=headers).json()


			for ch in data["data"]["children"]:
				pic_url = ch["data"].get("url_overridden_by_dest")
				if pic_url:
					file_name = pic_url.split("/")[-1]
					if not "." in file_name:
						continue
					with open(file_name, "wb") as f_out:
						c = requests.get(pic_url, headers=headers).content
						f_out.write(c)

			photos = []
			photos.clear()

			for x in os.listdir("."):
				if x.endswith(".jpg") or x.endswith(".png"):
					photos.append(x)

			await app.send_photo(m.chat.id, random.choice(photos))

			# finally remove
			for x in os.listdir("."):
				if x.endswith(".jpg") or x.endswith(".png"):
					os.remove(x)

		except Exception as e:
			await app.error(m, e)

	elif app.textlen(m) > 4096:
		return await app.send_edit(m, "Too long query, only 4096 characters are allowed !", delme=2)
	else:
		await app.send_edit(m, "Try again later !", delme=2)


