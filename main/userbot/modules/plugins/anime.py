import json
import requests

from pyrogram.types import Message

from main import app, gen





anime_suffix = "`baka`\n`bite`\n`blush`\n`bored`\n`cry`\n`cuddle`\n`dance`\n`facepalm`\n`feed`\n`happy`\n`highfive`\n`hug`\n`kiss`\n`laugh`\n`pat`\n`poke`\n`pout`\n`shrug`\n`slap`\n`sleep`\n`smile`\n`stare`\n`think`\n`thumbsup`\n`tickle`\n`wave`\n`wink`"
anime_list = ["baka", "bite", "blush", "bored", "cry", "cuddle", "dance", "facepalm", "feed", "happy", "highfive", "hug", "kiss", "laugh", "pat", "poke", "pout", "shrug", "slap", "sleep", "smile", "stare", "think", "thumbsup", "tickle", "wave", "wink"]




app.CMD_HELP.update(
    {"anime": (
        "anime",
        {
        "npic" : "Get a anime neko girl image.",
        "animegif [suffix]" : "Get gif's of different anime expressions, use the command below to get suffix list.",
        "animelist":"Get list of supported suffix for animegif command."
        }
        )
    }
)






def get_anime_gif(arg):
    data = requests.get(f"https://nekos.best/api/v2/{arg}").json()
    data = data["results"][0]
    img = data["url"]
    text = data["anime_name"]
    if img and text:
        return [img, text]
    else:
        return None



async def send_gif(m: Message, gif_data):
    try:
        await app.send_video(
            m.chat.id,
            gif_data[0],
            caption=gif_data[1]
        )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("animelist", allow = ["sudo"]))
async def animelist(_, m: Message):
    await app.send_edit(anime_suffix)



    
@app.on_message(gen(["nekopic", "npic"], allow = ["sudo"]))
async def nekoanime(_, m: Message):
    try:
        if m.from_user.is_self:
            await m.delete()

        data = requests.get("https://nekos.best/api/v2/neko").json()
        data = data["results"][0]
        await app.send_photo(
            m.chat.id,
            data["url"],
            caption = data["artist_name"]
            )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("animegif", allow = ["sudo"]))
async def animegif(_, m: Message):
    if app.long() > 1:
        arg = m.command[1]
        try:
            if m.from_user.is_self:
                await m.delete()

            if arg in anime_list:
                data = get_anime_gif(arg)
                await send_gif(m, data)
            else:
                await app.send_edit(anime_suffix)
        except Exception as e:
            await app.error(e)
    else:
        await app.send_edit(f"Give me a suffix, use `{app.Trigger()[0]}animelist` to get suffix.", delme=3)
