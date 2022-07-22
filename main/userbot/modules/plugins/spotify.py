from main import app, gen

from pyrogram.types import Message

from pyfy import AsyncSpotify




async def spotify_now():
    token = app.SpotifyToken()

    spt = AsyncSpotify(token)
    data = await spt.currently_playing()

    if not data:
        return {}

    info = data["item"]
    name = "**Song:**" + info["name"] + "\n\n"
    artist = "**Artists:**" + ", ".join([x["name"] for x in info["album"]["artists"]]) + "\n\n"
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
    if not app.SpotifyToken():
        return await app.send_edit("Please fill `SPOTIFY_TOKEN var.", text_type=["mono"], delme=3)

    data = await spotify_now()
    if not data:
        return await app.send_edit("You are not listening to anything.", text_type=["mono"], delme=3)

    caption = data["song_name"]
    caption += data["artist_name"]
    caption += data["track_url"]

    await app.send_photo(
        m.chat.id,
        photo=data["image_url"],
        caption=caption
    )
