import asyncio
from pyrogram.types import Message

from main import app, gen
import requests

from bs4 import BeautifulSoup




app.CMD_HELP.update(
    {"song" : (
        "song",
        {
        "ly [song title]" : "Get Song Lyrics [ Japanese Songs Doesn't Work For Now.]",
        "song [song name]" : "Get songs in mp3 format.",
        "dz [song name]" : "Get songs from deezer bot in mp3 format."
        }
        )
    }
)


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
}



@app.on_message(gen(["song", "music"], exclude = ["sudo", "channel"]))
async def song_handler(_, m: Message):
    await app.send_edit("Getting song . . .")
    try:
        cmd = m.command
        reply = m.reply_to_message
        if app.long() > 1:
            song_name = m.text.split(None, 1)[1]
        elif reply and app.long() == 1:
            song_name = reply.text or reply.caption
        elif not reply and app.long() == 1:
            return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

        song_results = await app.get_inline_bot_results("audio_storm_bot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await app.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
            )

            # forward as a new message from Saved Messages
            saved = await app.get_messages("me", int(saved.updates[1].message.id))
            reply_to = m.reply_to_message.message_id if m.reply_to_message else None

            await app.send_audio(
                chat_id=m.chat.id,
                audio=str(saved.audio.file_id),
                reply_to_message_id=reply_to,
                caption=f"**Song:** `{song_name}`\n**Uploaded By:** {app.UserMention()}",
            )

            # delete the message from Saved Messages
            await app.delete_messages("me", saved.message_id)
        except TimeoutError:
            return await app.send_edit("Something went wrong, tru again !")
    except Exception as e:
        await app.error(e)
        await app.send_edit("failed to process your request, please check logs")




@app.on_message(gen(["dz", "deezer"], exclude = ["sudo", "channel"]))
async def deezer_handler(_, m: Message):
    try:
        await app.send_edit("Searching on deezer . . .")
        cmd = m.command
        reply = m.reply_to_message
        if app.long() > 1:
            song_name = m.text.split(None, 1)[1]
        elif reply and app.long() == 1:
            song_name = reply.text or reply.caption
        elif not reply and app.long() == 1:
            return await app.send_edit("Give a song name . . .", delme=3, text_type=["mono"])

        song_results = await app.get_inline_bot_results("DeezerMusicBot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await app.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
            )

            # forward as a new message from Saved Messages
            saved = await app.get_messages("me", int(saved.updates[1].message.id))
            reply_to = m.reply_to_message.id if m.reply_to_message else None

            await app.send_audio(
                chat_id=m.chat.id,
                audio=str(saved.audio.file_id),
                reply_to_message_id=reply_to,
                caption=f"**Song:** `{song_name}`\n**Uploaded By:** {app.UserMention()}",
            )

            # delete the message from Saved Messages
            await app.delete_messages("me", [saved.id, m.id])
        except TimeoutError:
            return await app.send_edit("Something went wrong, try again . . .", delme=3, text_type=["mono"])
    except Exception as e:
        await app.error(e)
        await app.send_edit("Something went wrong, try again !", text_type=["mono"], delme=3)




@app.on_message(gen(["ly", "lyrics"], exclude = ["sudo", "channel"]))
async def lyrics_handler(_, m: Message):
    try:
        cmd = m.command
        reply = m.reply_to_message

        if not reply and len(cmd) > 1:
            song_name = m.text.split(None, 1)[1]

        elif reply:
            if reply.audio:
                song_name = f"{reply.audio.title} {reply.audio.performer}"
            elif reply.text or reply.caption and len(cmd) == 1:
                song_name = reply.text or reply.caption
            elif reply.text and len(cmd) > 1:
                song_name = m.text.split(None, 1)[1]
            else:
                return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

        elif not reply and len(cmd) == 1:
            return await app.send_edit("Give me a song name . . .", text_type=["mono"], delme=3)

        await app.send_edit(f"**Finding lyrics for:** `{song_name}`")

        url = "https://www.google.com/search?q="
        raw = requests.get(url + song_name.replace(" ", "%20") + "%20lyrics", headers=headers).text
        soup = BeautifulSoup(raw, "html.parser")
        content = soup.find_all("div", {"class":"ujudUb"})

        if not content:
                return await app.send_edit(f"No lyrics found ! for song: {song_name}", text_type=["mono"], delme=3)
        else:
                await app.send_edit("".join([x.text for x in content]), text_type=["mono"])
    except Exception as e:
        await app.error(e)
        await app.send_edit("Something went wrong, please try again later !", text_type=["mono"], delme=3)
