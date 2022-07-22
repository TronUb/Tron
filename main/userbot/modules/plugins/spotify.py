from main import app, gen

from pyrogram.types import Message
from pyrogram.enums.ChatType import (
    SUPERGROUP,
    GROUP
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pyfy import AsyncSpotify




async def spotify_now():
    token = app.SpotifyToken()

    spt = AsyncSpotify(token)
    data = await spt.currently_playing()

    if not data:
        return {}

    info = data["item"]
    name = "**Song:** " + info["name"] + "\n\n"
    artist = "**Artists:** " + ", ".join([x["name"] for x in info["album"]["artists"]]) + "\n\n"
    image_url = info["album"]["images"][0]["url"]
    track_url = info["external_urls"]["spotify"]

    return {
        "song_name":name,
        "artist_name":artist,
        "image_url":image_url,
        "track_url":track_url
        }




@app.on_message(gen("now", exclude=["sudo", "channel"]))
async def spotify_handler(_, m: Message):
    try:
        if not app.SpotifyToken():
            return await app.send_edit("Please fill `SPOTIFY_TOKEN var.", text_type=["mono"], delme=3)

        data = await spotify_now()
        if not data:
            return await app.send_edit("You are not listening to anything.", text_type=["mono"], delme=3)

        caption = f"**{app.name}**\n"
        caption += "`is listening to`\n\n"
        caption += f"**{data["song_name"]}**\n"
        caption += f"**By** `{data["artist_name"]}`\n\n"
        track_url = data["track_url"]

        if m.chat.type in (SUPERGROUP, GROUP):
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
    except Exception as e:
        await app.error(e)

