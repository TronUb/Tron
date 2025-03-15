import requests
from pyrogram.types import Message
from main import app

anime_suffix = """
`baka`  `bite`  `blush`  `bored`  `cry`  `cuddle`
`dance`  `facepalm`  `feed`  `happy`  `highfive`  `hug`
`kiss`  `laugh`  `pat`  `poke`  `pout`  `shrug`
`slap`  `sleep`  `smile`  `stare`  `think`  `thumbsup`
`tickle`  `wave`  `wink`
"""
anime_list = [x.strip("` ") for x in anime_suffix.split()]


def get_anime_gif(action):
    try:
        response = requests.get(f"https://nekos.best/api/v2/{action}", timeout=10)
        response.raise_for_status()
        data = response.json()["results"][0]
        return [data["url"], data["anime_name"]]
    except (requests.RequestException, KeyError, IndexError):
        return None


async def send_gif(m: Message, gif_data):
    if gif_data:
        try:
            await app.send_video(m.chat.id, gif_data[0], caption=gif_data[1])
        except Exception as e:
            await app.error(e)
    else:
        await app.send_edit("Failed to fetch the anime GIF.")


@app.on_cmd(commands="animelist", usage="Get list of available keywords.")
async def animelist_handler(_, m: Message):
    await app.send_edit(anime_suffix)


@app.on_cmd(commands=["nekopic", "npic"], usage="Get anime neko girl images.")
async def nekopic_handler(_, m: Message):
    try:
        await app.send_edit("Getting a neko girl image...", text_type=["mono"])
        response = requests.get("https://nekos.best/api/v2/neko", timeout=10)
        response.raise_for_status()
        data = response.json()["results"][0]
        await app.send_photo(
            m.chat.id, data["url"], caption=data.get("artist_name", "Unknown Artist")
        )
        await m.delete()
    except requests.RequestException as e:
        await app.error(f"API request failed: {e}")
    except Exception as e:
        await app.error(e)


@app.on_cmd(commands="animegif", usage="Get anime GIFs.")
async def animegif_handler(_, m: Message):
    try:
        if len(m.command) < 2:
            return await app.send_edit(
                "Usage: `.animegif <action>`\n\nUse these actions:\n" + anime_suffix
            )

        action = m.command[1].strip().lower()
        if action in anime_list:
            await app.send_edit(f"Fetching `{action}` anime GIF...", text_type=["mono"])
            data = get_anime_gif(action)
            await send_gif(m, data)
            await m.delete()
        else:
            await app.send_edit("Invalid action! Use these actions:\n" + anime_suffix)
    except Exception as e:
        await app.error(e)
