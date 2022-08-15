""" reddit plugin """

import os
import random
import requests
from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"reddit" : (
        "reddit",
        {
        "r [query]" : "Get reddit images (limit = 1)"
        }
        )
    }
)




@app.on_message(gen(["r", "reddit"]))
async def reddit_handler(_, m: Message):
    """ reddit handler for reddit plugin """
    if app.long() == 1:
        return await app.send_edit("Please give me some query to search on reddit.", delme=2)

    elif app.textlen() > 4096:
        return await app.send_edit(
            "Too long query, only 4096 characters are excludeed !",
            text_type=["mono"],
            delme=3
        )

    elif app.long() > 1:
        try:
            query = m.text.split(None, 1)[1]
            await app.send_edit("Getting reddit images . . .", text_type=["mono"])
            url = f"https://old.reddit.com/r/{query}.json"
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
                        kate = requests.get(pic_url, headers=headers).content
                        f_out.write(kate)

            photos = [x for x in os.listdir(".") if x.endswith(".jpg") or x.endswith(".png") or x.endswith(".gif") or ""]
            await app.send_photo(m.chat.id, random.choice(photos))

            # finally remove
            for x in os.listdir("."):
                if x.endswith(".jpg") or x.endswith(".png") or x.endswith(".gif"):
                    os.remove(x)

            await m.delete()

        except Exception as e:
            await app.error(e)
