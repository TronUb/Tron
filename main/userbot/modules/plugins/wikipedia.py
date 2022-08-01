import time
import wikipediaapi

from pyrogram.types import Message

from main import app, gen




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
async def wikipedia_handler(_, m: Message):
    if app.long() == 1:
        await app.send_edit("Give me some query to search on wikipedia . . .", text_type=["mono"], delme=True)

    elif app.long() > 1 and app.long() < 4096:
        try:
            obj = wikipediaapi.Wikipedia("en")
            text = m.text.split(None, 1)[1]
            result = obj.page(text)
            await app.send_edit(f"Searching for: __{text}__ . . .", text_type=["mono"])
            if result:
                giveresult = result.summary
                if len(giveresult) <= 4096:
                    await app.send_edit(f"**Results for:** `{text}`\n\n```{giveresult}```")
                else:
                    await app.send_edit(f"**Results for:** `{text}`\n\n```{giveresult[:4095]}```")
            else:
                await app.send_edit("No results found !", delme=2, text_type=["mono"])
        except Exception as e:
            await app.error(e)
    else:
        await app.send("Something went wrong !", text_type=["mono"], delme=3)
