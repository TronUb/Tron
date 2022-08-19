import os
import re
from moviepy.editor import *

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"videotools" : (
        "videotools",
        {
            "vcut [reply] [hh:mm:ss]":"Cut video at desired duration",
            "vinvert [reply]":"Invert colour of video",
            "vmute [reply]":"Mute audio of downloaded video",
            "vsubclip [reply] [hh:mm:ss] [hh:mm:ss]":"Cut sub clip of a video",
            "vafadein [reply] [duration]":"Add fade in effect to the audio of video.",
            "vafadeout [reply] [duration]":"Add fade out effect to the audio of video.",
            "vsetaudio [reply] [audio path]":"Set a new audio to video.",
            "vspeed [times]":"Increase or decrease video speed",
            "vfadein [duration]":"Add video fade in effect",
            "vfadeout [duration]":"Add video fade out effect"
        }
        )
    }
)




pattern = r"([0-9]{2}:){2}[0-9]{2}"


def Video(path):
    return VideoFileClip(path)


def Audio(path):
    return AudioFileClip(path)


async def send_delete(text):
    return await app.send_edit(
        text,
        text_type=["mono"],
        delme=3
    )


def not_reply(message):
    reply = message.reply_to_message

    if not reply:
        return True
    
    if not reply.video:
        return True

    return None



async def send_video(message, filename, text):
    if os.path.exists(filename):
        msg = await app.send_edit(
            "Sending new video . . .",
            text_type=["mono"]
        )
        await app.send_video(
            message.chat.id,
            filename
        )
        os.remove(filename)
        return await msg.delete()
    else:
        return await send_delete(
            text
        )




@app.on_message(gen("vcut"))
async def vcut_handler(_, m: Message):
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
            m,
            filename,
            "Failed to cut video, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vinvert"))
async def vinvert_handler(_, m: Message):
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
            m,
            filename,
            "Failed to invert video, try again later !"
        )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("vmute"))
async def vmute_handler(_, m: Message):
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
            m,
            filename,
            "Failed to mute video, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vsubclip"))
async def vsubclip_handler(_, m: Message):
    """ video sub clip cut hanlder for videotools plugin  """
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
            _, start_time, end_time = args.text.split()
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
            m,
            filename,
            "Failed to cut sub clip of video, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vafadein"))
async def vafadein_handler(_, m: Message):
    """ video's audio fade in hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeinvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade in duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding fade in to video . . .",
            text_type=["mono"]
        )

        v_time = clip.duration
        if duration > v_time:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.audio_fadein(duration)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade in effect in video, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vafadeout"))
async def vafadeout_handler(_, m: Message):
    """ video's audio fade out hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeoutvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding fade out to video . . .",
            text_type=["mono"]
        )

        if duration > clip.duration:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.audio_fadeout(duration)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade out effect in video audio, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vsetaudio"))
async def vsetaudio_handler(_, m: Message):
    """ set audio to video hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/setaudiovideo.mp4"
    
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
            _, audio_path = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not os.path.exists(audio_path):
            return await send_delete(
                "The audio doesn't exist."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        audio
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding a new audio to the video . . .",
            text_type=["mono"]
        )

        audio = Audio(audio_path)
        clip = clip.set_audio(audio)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade out effect in video audio, try again later !"
        )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("vmute"))
async def vmute_handler(_, m: Message):
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
            m,
            filename,
            "Failed to mute video, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vsubclip"))
async def vsubclip_handler(_, m: Message):
    """ video sub clip cut hanlder for videotools plugin  """
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
            _, start_time, end_time = args.text.split()
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
            m,
            filename,
            "Failed to cut sub clip of video, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vafadein"))
async def vafadein_handler(_, m: Message):
    """ video's audio fade in hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeinvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade in duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding fade in to video . . .",
            text_type=["mono"]
        )

        v_time = clip.duration
        if int(duration) > v_time:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.audio_fadein(int(duration))
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade in effect in video, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vafadeout"))
async def vafadeout_handler(_, m: Message):
    """ video's audio fade out hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeoutvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding fade out to video . . .",
            text_type=["mono"]
        )

        if int(duration) > clip.duration:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.audio_fadeout(int(duration))
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade out effect in video audio, try again later !"
        )
    except Exception as e:
        await app.error(e)





@app.on_message(gen("vsetaudio"))
async def vsetaudio_handler(_, m: Message):
    """ set audio to video hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/setaudiovideo.mp4"
    
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
            _, audio_path = args.text.split(None, 1)
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not os.path.exists(audio_path):
            return await send_delete(
                "The audio doesn't exist."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding a new audio to the video . . .",
            text_type=["mono"]
        )

        audio = Audio(audio_path)
        clip = clip.set_audio(audio)
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade out effect in video audio, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vspeed"))
async def vspeed_handler(_, m: Message):
    """ video speed hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/speedvideo.mp4"
    
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
            _, video_speed = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper speed time."
            )

        if not video_speed.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Speeding up the video . . .",
            text_type=["mono"]
        )

        clip = clip.speedx(int(video_speed))
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to speed the video, try again later !"
        )
    except Exception as e:
        await app.error(e)



@app.on_message(gen("vfadeout"))
async def vfadeout_handler(_, m: Message):
    """ video fade out hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeoutvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding fade out to video . . .",
            text_type=["mono"]
        )

        if int(duration) > clip.duration:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.fadeout(int(duration))
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade out effect in video, try again later !"
        )
    except Exception as e:
        await app.error(e)


@app.on_message(gen("vfadein"))
async def vfadein_handler(_, m: Message):
    """ video fade in hanlder for videotools plugin  """
    try:
        reply = m.reply_to_message
        filename = "./downloads/fadeinvideo.mp4"
    
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
            _, duration = args.text.split()
        except IndexError:
            return await send_delete(
                "Give me the proper fade out duration."
            )

        if not duration.isdigit():
            return await send_delete(
                "The duration must be a integer (seconds)."
            )

        await app.send_edit(
            "Downloading video . . .",
            text_type=["mono"]
        )
        clip = Video(await reply.download())
        await app.send_edit(
            "Adding in effect out to video . . .",
            text_type=["mono"]
        )

        if int(duration) > clip.duration:
            return await send_delete(
                "The given duration can't be greater than the video duration."
            )

        clip = clip.fadein(int(duration))
        await app.send_edit(
            "Saving new video . . .",
            text_type=["mono"]
        )

        clip.write_videofile(filename)

        await send_video(
            m,
            filename,
            "Failed to add fade in effect in video, try again later !"
        )
    except Exception as e:
        await app.error(e)

