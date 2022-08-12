from main import app, gen

from pytube import YouTube
from pytube.exceptions import LiveStreamError

from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.enums import MessageEntityType, ChatType

from PIL import Image




app.CMD_HELP.update(
    {"utube": (
        "utube",
        {
        "ytvinfo [ link | reply ]" : "Get a youtube video information.",
        "ytmdl [ link | reply ] [ -a ]" : "Download any video/audio from YouTube Use flag -a to download audio. If your bot is present in chat, by default you'll get inline results.",
        }
        )
    }
)



def ResizeImage(path: str, size: tuple=(320, 320)):
    img = Image.open(path)
    img.thumbnail(size)
    photo = app.TEMP_DICT+"photo.jpg"
    img.save(photo)
    return photo





@app.on_message(gen("ytvinfo"))
async def ytvideoinfo_handler(_, m: Message):
    try:
        args = app.GetArgs()
        if args:
            if args.text and args.text.entities:
                entity = args.text.entities
                if entity[0].type == MessageEntityType.URL:
                    i = entity[0]
                    link = args.text[i.offset:i.length+i.offset] # get link from text
                else:
                    link = args.text
            else:
                link = args.text
        else:
            return await app.send_edit("Reply or give args after command.", text_type=["mono"], delme=3)

        await app.send_edit("Getting information . . .", text_type=["mono"])
        yt = YouTube(link)
        thumb_link = yt.thumbnail_url
        data = f"**Title:** {yt.title}\n\n"
        data += f"**Duration:** {app.GetReadableTime(yt.length)}\n\n"
        data += f"**Description:** {yt.description[:500]}...\n\n"
        data += f"**Views:** {yt.views}\n\n"
        data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

        await app.send_photo(m.chat.id, thumb_link, caption=data)
    except Exception as e:
        await app.error(e)




@app.on_message(gen("ytmdl"))
async def ytmdl_handler(_, m):
    try:
        msg = await app.send_edit("processing link . . .", text_type=["mono"])
        reply = m.reply_to_message
        cmd = m.command
        args = app.GetArgs(m)

        if not args:
            return await app.send_edit(
                "Reply or give args after command.",
                text_type=["mono"],
                delme=3
            )

        if not args.text:
            return await app.send_edit(
                "there is not text in this command.",
                text_type=["mono"],
                delme=3
            )

        if not args.text.entities:
            return await app.send_edit(
                "There are no youtube urls in message or wrong youtube link.",
                text_type=["mono"],
                delme=3
            )

        link = None
        entity = args.text.entities
        if entity[0].type == MessageEntityType.URL:
            i = entity[0]
            link = args.text[i.offset:i.length+i.offset] # get link from text

        if not link:
            return await app.send_edit(
                "There is no link.",
                text_type=["mono"],
                delme=3
            )

        yt = YouTube(link)
        path = app.PyDownload(yt.thumbnail_url)
        thumbnail = ResizeImage(path)

        try:
            data = yt.streams
        except LiveStreamError:
            return await app.send_edit(
                "The owner of this channel is doing live stream, can't download the media.",
                text_type=["mono"],
                delme=3
            )

        if m.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            if await app.user_exists(m.chat.id, app.bot.id):
                botmsg = await app.bot.send_message(chat_id=m.chat.id, text="`processing link . . .`")

                buttons = []
                temp = []

                for x in range(len(data)):
                    name = data[x]
                    
                    if name.resolution:
                        btn = app.BuildKeyboard(([
                            [
                                str(name.resolution) + " 🔇" if not name.includes_audio_track else str(name.resolution), 
                                str(name.itag)
                            ]
                        ]))
                    elif name.abr:
                        btn = app.BuildKeyboard(([
                            [
                                str(name.abr), 
                                str(name.itag)
                            ]
                        ]))
                    else:
                        continue

                    if len(temp) < 3:
                        temp.append(btn[0])
                    if len(temp) == 3:
                        buttons.append(temp)
                        temp = []

                await msg.delete()
                await app.bot.send_photo(chat_id=m.chat.id, photo=path, caption=f"**Title:** {yt.title}", reply_markup=InlineKeyboardMarkup(buttons))
                await botmsg.delete()
                app.bot.utube_object = data

                async def utube_callback(client, cb):
                    try:
                        
                        if not cb.from_user.id == m.from_user.id:
                            await cb.answer("You're not excludeed.", show_alert=True)
                            return False

                        if (int(cb.data) in [int(x.itag) for x in client.utube_object]):
                            obj = client.utube_object.get_by_itag(int(cb.data))
                            botmsg = await client.send_message(cb.message.chat.id, f"`Uploading {obj.type} . . .`")

                            if obj.type == "video":
                                loc = obj.download(client.TEMP_DICT)
                                await client.send_video(chat_id=cb.message.chat.id, video=loc, caption="**Title:**\n\n" + loc.split("/")[-1], thumb=thumbnail)
                            elif obj.type == "audio":
                                loc = obj.download(client.TEMP_DICT, f"{obj.title.split('.')[0]}.mp3")
                                await client.send_audio(chat_id=cb.message.chat.id, audio=loc, caption="**Title:**\n\n" + loc.split("/")[-1], thumb=thumbnail)
                            await botmsg.delete()
                        else:
                            await cb.answer("The message is expired.", show_alert=True)
                    except Exception as e:
                        print(e)
                        await client.error(e)

                app.bot.add_handler(CallbackQueryHandler(callback=utube_callback, filters=filters.regex(r"^\d+")))
                return True

        media_found = False
        msg = await app.send_edit("**Trying to download **" + f"`{yt.title}`")
        media_type = "audio" if app.long() > 1 and "-a" in m.text else "video"

        for x in data:
            if media_type == "video":
                if x.type == "video" and x.resolution in ("720p", "1080p") and x.mime_type == "video/mp4":
                    media_found =True
                    loc = x.download(app.TEMP_DICT, f"{yt.title.split('.')[0]}.mp4")
                    await app.send_video(m.chat.id, loc, caption="**Title:**\n\n" + yt.title, thumb=thumbnail)
                    await msg.delete()
                    break

            elif media_type == "audio":
                if x.type == "audio" and x.abr in ("128kbps", "160kbps", "250kbps", "70kbps") and x.mime_type in ("audio/webm", "audio/mpeg"):
                    media_found =True
                    loc = x.download(app.TEMP_DICT, f"{yt.title.split('.')[0]}.mp3")
                    await app.send_audio(m.chat.id, loc, caption="**Title:**\n\n" + yt.title, thumb=thumbnail)
                    await msg.delete()
                    break

        if not media_found:
            await app.send_edit(f"I didn't found any good quality {media_type} of this YouTube link", text_type=["mono"], delme=3)   
    except Exception as e:
        await app.error(e)
