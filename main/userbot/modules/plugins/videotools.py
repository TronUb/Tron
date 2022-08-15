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



@app.on_message(gen("vcut"))
async def videocut_handler(_, m: Message):
    """ video cut hanlder for videotools plugin  """
    reply = m.reply_to_message
    vname = "./downloads/cutvideo.mp4"

    await app.send_edit(
        "Processing . . .",
        text_type=["mono"]
    )

    if not (reply or reply.video):
        return await app.send_edit(
            "Reply to a video . . .",
            text_type=["mono"],
            delme=3
        )

    args = app.GetArgs(m)
    if not args:
        return await app.send_edit(
            "Something went wrong, try again later.",
            text_type=["mono"],
            delme=3
        )

    cut_time = args.text.split(None, 1)[0]

    msg = await app.send_edit(
        "Downloading video . . .",
        text_type=["mono"]
    )
    clip = Video(await reply.download())
    msg = await msg.edit(
        "Cutting video . . .",
        text_type=["mono"]
    )

    clip = clip.set_duration(cut_time)
    msg = await msg.edit(
        "Saving new video . . .",
        text_type=["mono"]
    )

    clip.write_videofile(vname)

    if os.path.exists(vname):
        await msg.edit(
            "Ssnding new video . . .",
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

