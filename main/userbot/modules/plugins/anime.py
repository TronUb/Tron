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
    """ 
        name:: 
            get_anime_gif
        
        parameters::
            arg (str): a query to search
            
        returns::
            list | None
    """
    data = requests.get(f"https://nekos.best/api/v2/{arg}").json()
    data = data["results"][0]
    img = data["url"]
    text = data["anime_name"]
    if img and text:
        return [img, text]
    else:
        return None



async def send_gif(m: Message, gif_data):
    """ 
        name:: 
            send_gif
        
        parameters::
            message (pyrogram.types.Message): pyrogram message
            gif_data (list):: a list containing image url and text
            
        returns::
            None
    """
    try:
        await app.send_video(
            m.chat.id,
            gif_data[0],
            caption=gif_data[1]
        )
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="animelist"
    )
)
async def animelist_handler(_, m: Message):
    """
        name::
            animelist_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    await app.send_edit(anime_suffix)




@app.on_message(
    gen(
        commands=["nekopic", "npic"]

    )
)
async def nekopic_handler(_, m: Message):
    """
        name::
            nekopic_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
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




@app.on_message(
    gen(
        commands="animegif",
        max_args=1
    )
)
async def animegif_handler(_, m: Message):
    """
        name::
            animegif_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
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