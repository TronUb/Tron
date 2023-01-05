""" anime plugin """

import requests

from pyrogram.types import Message

from main import app, gen



anime_suffix = "`baka`\n`bite`\n`blush`\n`bored`\n`cry`\n`cuddle`\n`dance`\n`facepalm`\n`feed`\n`happy`\n`highfive`\n`hug`\n`kiss`\n`laugh`\n`pat`\n`poke`\n`pout`\n`shrug`\n`slap`\n`sleep`\n`smile`\n`stare`\n`think`\n`thumbsup`\n`tickle`\n`wave`\n`wink`"
anime_list = [
    "baka",
    "bite",
    "blush",
    "bored",
    "cry",
    "cuddle",
    "dance",
    "facepalm",
    "feed",
    "happy",
    "highfive",
    "hug",
    "kiss",
    "laugh",
    "pat",
    "poke",
    "pout",
    "shrug",
    "slap",
    "sleep",
    "smile",
    "stare",
    "think",
    "thumbsup",
    "tickle",
    "wave",
    "wink"
]


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




@app.on_cmd(
    commands="animelist",
    usage="Get list of available keywords."
)
async def animelist_handler(_, m: Message):
    await app.send_edit(anime_suffix)




@app.on_cmd(
    commands=["nekopic", "npic"],
    usage="Get anime neko girl images."
)
async def nekopic_handler(_, m: Message):

    try:
        data = requests.get("https://nekos.best/api/v2/neko").json()
        data = data["results"][0]
        await app.send_photo(
            m.chat.id,
            data["url"],
            caption = data["artist_name"]
        )
        await m.delete()
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands="animegif",
    ussge="Get anime gifs."
)
async def animegif_handler(_, m: Message):

    try:
        arg = m.command[1]

        if arg in anime_list:
            data = get_anime_gif(arg)
            await send_gif(m, data)
            await m.delete()
        else:
            await app.send_edit("Use these suffix only:\n\n" + anime_suffix)
    except Exception as e:
        await app.error(e)
