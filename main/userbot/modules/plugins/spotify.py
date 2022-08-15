""" spotify plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pyfy import AsyncSpotify

from main import app, gen




async def spotify_now():
    """ spotify now function for spotify plugin """
    token = app.SpotifyToken()

    spt = AsyncSpotify(token)
    data = await spt.currently_playing()

    if not data:
        return {}

    info = data["item"]
    name = "**Song:**" + " " + info["name"] + "\n"
    artist = "**Artists:**" + " " + ", ".join([x["name"] for x in info["album"]["artists"]]) + "\n"
    image_url = info["album"]["images"][0]["url"]
    track_url = info["external_urls"]["spotify"]

    return {
        "song_name":name,
        "artist_name":artist,
        "image_url":image_url,
        "track_url":track_url
        }




@app.on_message(gen("now"))
async def spotify_handler(_, m: Message):
    """ spotify handler for spotify plugin """
    try:
        if not app.SpotifyToken():
            return await app.send_edit(
                "Please fill `SPOTIFY_TOKEN var.",
                text_type=["mono"],
                delme=3
            )

        data = await spotify_now()
        if not data:
            return await app.send_edit(
                "You are not listening to anything.",
                text_type=["mono"],
                delme=3
            )

        caption = f"{app.name}\n"
        caption += "is listening to\n\n"
        caption += f"{data['song_name']}\n"
        caption += f"{data['artist_name']}\n\n"
        track_url = data["track_url"]

        if m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            if await app.user_exists(m.chat.id, app.bot.id):
                return await app.bot.send_photo(
                    m.chat.id,
                    photo=data["image_url"],
                    caption=caption,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Play on Spotify",
                                    url=track_url
                                )
                            ]
                        ]
                    )
                )

        await app.send_photo(
            m.chat.id,
            photo=data["image_url"],
            caption=caption+track_url
        )
        await m.delete()
    except Exception as e:
        await app.error(e)
