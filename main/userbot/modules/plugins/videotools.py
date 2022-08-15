import os
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



def Video(path):
    return VideoFileClip(path)


async def sendit(text):
    return await app.send_edit(
        text,
        text_type=["mono"],
        delme=3
    )


@app.on_message(gen("vcut"))
async def videocut_handler(_, m: Message):
    """ video cut hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        vname = "./downloads/cutvideo.mp4"
    
        await app.send_edit(
            "Processing . . .",
            text_type=["mono"]
        )

        if not reply:
            return await sendit(
                "Reply to a video . . ."
            )

        if not reply.video:
            return await sendit(
                "Reply to a video . . ."
            )

        args = app.GetArgs(m)
        if not args:
            return await sendit(
                "Something went wrong, try again later."
            )
        try:
            cut_time = args.text.split(None, 1)[1]
        except IndexError:
            return await sendit(
                "Give me the duration you want to cut."
            )

        if not ":" in cut_time:
            return await sendit(
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
            return await sendit(
                "The duration time is wrong, use `hh:mm:ss`"
            )

        if dv_time > v_time:
            return await sendit(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.set_duration(cut_time)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(vname)

        if os.path.exists(vname):
            msg = await app.send_edit(
                "Sending new video . . .",
                text_type=["mono"]
            )
            await app.send_video(
                m.chat.id,
                vname
            )
            os.remove(vname)
            await msg.delete()
        else:
            await app.send_edit(
                "Failed to cut video, try again !",
                text_type=["mono"],
                delme=3
            )
    except Exception as e:
        await app.error(e)
