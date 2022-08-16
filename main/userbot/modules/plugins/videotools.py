import os
import re
from moviepy.editor import *

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"dev" : (
        "dev",
        {
        "vcut":"Cut video at desired duration, cut format: `00:02:30`",
        
        }
        )
    }
)




pattern = r"([0-9]{2}:){2}[0-9]{2}"


def Video(path):
    return VideoFileClip(path)


async def send_delete(text):
    return await app.send_edit(
        text,
        text_type=["mono"],
        delme=3
    )


def not_reply(message):
    reply = message.reply_to_message

    if not reply:
        return None
    
    if not reply.video:
        return None


async def send_video(filename, text):
    if os.path.exists(filename):
        msg = await app.send_edit(
            "Sending new video . . .",
            text_type=["mono"]
        )
        await app.send_video(
            m.chat.id,
            filename
        )
        os.remove(filename)
        return await msg.delete()
    else:
        return await send_delete(
            text
        )




@app.on_message(gen("vcut"))
async def videocut_handler(_, m: Message):
    """ video cut hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/cutvideo.mp4"

        await app.send_edit(
            "Processing . . .",
            text_type=["mono"]
        )

        if not_reply(m):
            return await send_delete(
                "Reply to a video . . ."
            )

        args = app.GetArgs(m)
        if not args:
            return await send_delete(
                "Something went wrong, try again later."
            )

        try:
            cut_time = args.text.split(None, 1)[1]
        except IndexError:
            return await send_delete(
                "Give me the duration you want to cut."
            )

        if not re.match(pattern, cut_time):
            return await send_delete(
                "The duration time is wrong, use `hh:mm:ss`"
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Cutting video . . .",
            text_type=["mono"]
        )

        v_time = clip.duration
        t_list = [int(x) for x in cut_time.split(":")]
        try:
            dv_time = t_list[0]*60*60 + t_list[1]*60 + t_list[2]
        except IndexError:
            return await send_delete(
                "The duration time is wrong, use `hh:mm:ss`"
            )

        if dv_time > v_time:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.set_duration(cut_time)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            filename,
            "Failed to cut video, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vinvert"))
async def videoinvert_handler(_, m: Message):
    """ video color inverting hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/invertvideo.mp4"

        if not_reply(m):
            return await app.send_edit(
                "Reply to a video sir . . .",
                text_type=["mono"],
                delme=3
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())

        await app.send_edit(
            "Inverting video . . .",
            text_type=["mono"]
        )
        clip = clip.invert_colors()

        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )
        clip.write_videofile(filename)

        await send_video(
            filename,
            "Failed to invert video, try again later !"
        )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("vmute"))
async def videomute_handler(_, m: Message):
    """ video muting hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/mutevideo.mp4"

        if not reply:
            return await app.send_edit(
                "Reply to a video sir . . .",
                text_type=["mono"],
                delme=3
            )

        if not reply.video:
            return await app.send_edit(
                "Reply to a video sir . . .",
                text_type=["mono"],
                delme=3
            )
        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())

        await app.send_edit(
            "Muting audio of this video . . .",
            text_type=["mono"]
        )
        clip = clip.volumex(0)

        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )
        clip.write_videofile(filename)

        await send_video(
            filename,
            "Failed to mute video, try again later !"
        )
    except Exception as e:
        await app.error(e)


@app.on_message(gen("vsubclip"))
async def videocut_handler(_, m: Message):
    """ video cut hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/subclipvideo.mp4"
    
        await app.send_edit(
            "Processing . . .",
            text_type=["mono"]
        )

        if not_reply(m):
            return await send_delete(
                "Reply to a video . . ."
            )

        args = app.GetArgs(m)
        if not args:
            return await send_delete(
                "Something went wrong, try again later."
            )
        try:
            start_time = args.text.split(None, 1)[1]
            end_time = args.text.split(None, 2)[2]
        except IndexError:
            return await send_delete(
                "Give me the proper subclip duration."
            )

        if not (re.match(pattern, start_time) or
            re.match(pattern, end_time)
            ):
            return await send_delete(
                "The duration time is wrong, use `hh:mm:ss`"
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Cutting sub clip of video . . .",
            text_type=["mono"]
        )

        v_time = clip.duration
        t_list = [int(x) for x in end_time.split(":")]
        try:
            dv_time = (t_list[0]*60*60) + (t_list[1]*60) + t_list[2]
        except IndexError:
            return await send_delete(
                "The duration time is wrong, use `hh:mm:ss`"
            )

        if dv_time > v_time:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.subclip(start_time, end_time)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            filename,
            "Failed to cut sub clip of video, try again later !"
        ))
    except Exception as e:
        await app.error(e)

