""" download plugi """

import os
import time
import math
import asyncio
import traceback

from datetime import datetime
from pySmartDL import SmartDL

from pyrogram.types import Message

from pyrogram import errors

from main import app, gen




app.CMD_HELP.update(
    {"download" : (
        "download",
        {
        "ls [path]" : "Find file location in the local directories.",
        "download [Reply to media]" : "Downloads media files in local server.",
        "upload [path]" : "Upload files from local server to telegram",
        "batchup [path]" : "Upload batch files from a local directories."
        }
        )
    }
)





@app.on_message(gen("ls"))
async def ls_handler(_, m: Message):
    """ function to show directory files and folders """

    try:
        location = "." if app.long() == 1 else m.command[1] if m.command and app.long() >= 2 else None

        location = os.path.abspath(location)
        if not location.endswith("/"):
            location += "/"
        OUTPUT = f"**Files in** `{location}`:\n\n"

        await app.send_edit("Fetching files . . .", text_type=["mono"])

        try:
            files = os.listdir(location)
        except FileNotFoundError:
            return await app.send_edit(f"No such file or directory {location}", delme=2)

        collect = []
        collect.clear()

        for file in files:
            if (not file.endswith(".session") and
                not file in ["__pycache__", ".git", ".github", ".profile.d", ".heroku", ".cache"]):
                if os.path.isfile(f"{location}/{file}"):
                    collect.append(f"📑 `{file}` ({app.DictSize(os.path.abspath(location+file))})")
                if os.path.isdir(f"{location}/{file}"):
                    collect.append(f"🗂️ `{file}` ({app.DictSize(os.path.abspath(location+file))})")

        collect.sort() # sort the files
        file = "\n".join(collect)
        OUTPUT += f"{file}"

        if len(OUTPUT) > 4096:
            await m.delete()
            await app.create_file(app, filename="dict.txt", text=OUTPUT)
        elif OUTPUT.endswith("\n\n"):
            return await app.send_edit(f"No files in `{location}`", delme=4)
        elif len(OUTPUT) <= 4096:
            await app.send_edit(OUTPUT)
    except Exception as e:
        await app.error(e)





@app.on_message(gen(["download", "dl"]))
async def download_handler(_, m: Message):
    """ function to download media """

    reply = m.reply_to_message
    if reply and reply.media:
        try:
            start_t = datetime.now()
            c_time = time.time()

            await app.send_edit("• Downloading . . .", text_type=["mono"])
            location = await app.download_media(
                message=reply,
                progress=app.ProgressForPyrogram,
                progress_args=("Downloading file . . .", m, c_time),
            )

            end_t = datetime.now()
            duration = app.GetReadableTime((end_t - start_t).seconds)

            if location is None:
                await app.send_edit("Download failed, please try again.", text_type=["mono"])
            else:
                await app.send_edit(
                    f"**Downloaded to •>**\n\n```{location}```\n\n**Time:** `{duration}`"
                )
        except Exception as e:
            await app.error(e)
            await app.send_edit("Failed To Download, look in log chat for more info.")

    elif app.long() > 1:
        try:
            start_t = datetime.now()
            the_url_parts = " ".join(m.command[1:])
            url = the_url_parts.strip()
            custom_file_name = os.path.basename(url)
            if "|" in the_url_parts:
                url, custom_file_name = the_url_parts.split("|")
                url = url.strip()
                custom_file_name = custom_file_name.strip()
            download_file_path = os.path.join(app.TEMP_DICT, custom_file_name)
            downloader = SmartDL(url, download_file_path, progress_bar=False)
            downloader.start(blocking=False)
            c_time = time.time()
            while not downloader.isFinished():
                total_length = downloader.filesize if downloader.filesize else 0
                downloaded = downloader.get_dl_size()
                display_message = ""
                now = time.time()
                diff = now - c_time
                percentage = downloader.get_progress() * 100
                speed = downloader.get_speed(human=True)
                elapsed_time = round(diff) * 1000
                progress_str = "**[{0}{1}]**\n**Progress:** __{2}%__".format(
                    "".join(["●" for i in range(math.floor(percentage / 5))]),
                    "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
                    round(percentage, 2),
                )
                estimated_total_time = downloader.get_eta(human=True)
                try:
                    current_message = "__**Trying to download...**__\n"
                    current_message += f"**URL:** `{url}`\n"
                    current_message += f"**File Name:** `{custom_file_name}`\n"
                    current_message += f"{progress_str}\n"
                    current_message += (
                        f"__{app.HumanBytes(downloaded)} of {app.HumanBytes(total_length)}__\n"
                    )
                    current_message += f"**Speed:** __{speed}__\n"
                    current_message += f"**ETA:** __{estimated_total_time}__"
                    if round(diff % 10.00) == 0 and current_message != display_message:
                        await app.send_edit(
                            m,
                            disable_web_page_preview=True,
                            text=current_message
                        )
                        display_message = current_message
                        await asyncio.sleep(2)
                except errors.MessageNotModified:
                    pass
                except Exception as e:
                    app.log.info(str(e))

            await app.send_edit("• Downloading . . .", text_type=["mono"])
            if os.path.exists(download_file_path):
                end_t = datetime.now()
                ms = (end_t - start_t).seconds
                await app.send_edit(
                    f"**Downloaded to:** `{download_file_path}`\n**Time Taken:** `{ms}` seconds.\nDownload Speed: {round((total_length/ms), 2)}"
                )
        except Exception:
            exc = traceback.format_exc()
            return await app.send_edit(f"Failed Download!\nERROR:\n{exc}")
    else:
        await app.send_edit(
            "Reply to a Telegram Media to download it to local server.",
            text_type=["mono"],
            delme=4
        )





@app.on_message(gen(["upload", "ul"], exclude=["sudo"]))
async def upload_handler(_, m: Message):
    """ function to upload files from downloads """

    photo_ext = (".jpeg", "jpg", ".png", ".gif", "reply_photo")
    video_ext = (".mp4", ".mkv", "reply_video")
    sticker_ext = (".webp", "reply_sticker")
    audio_ext = (".ogg", ".flac", ".mp3", "reply_audio")
    animation_ext = (".tgs", "reply_animation")

    extensions = (photo_ext, video_ext, sticker_ext, audio_ext, animation_ext)

    if app.long() > 1:
        local_file_name = m.text.split(None, 1)[1]

        method = "reply_document"
        for x in range(len(extensions)):
            for y in range(len(extensions[x])):
                if local_file_name.endswith(extensions[x][y]):
                    method = extensions[x][-1]

        if os.path.exists(local_file_name):
            await app.send_edit("Uploading . . .", text_type=["mono"])
            start_t = datetime.now()
            doc_caption = os.path.basename(local_file_name)
            c_time = time.time()
            await app.send_edit(f"Uploading `{doc_caption}` . . .")

            if method == "reply_sticker":
                await m.reply_sticker(
                    local_file_name,
                    disable_notification=True,
                    reply_to_message_id=m.id,
                    progress=app.ProgressForPyrogram,
                    progress_args=("Uploading file . . .", m, c_time),
                )
            else:
                await getattr(m, method, None)(
                    local_file_name,
                    caption=doc_caption,
                    disable_notification=True,
                    reply_to_message_id=m.id,
                    progress=app.ProgressForPyrogram,
                    progress_args=("Uploading file . . .", m, c_time),
                )

            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await app.send_edit(f"Uploaded in `{ms}` seconds.", delme=4)
        else:
            await app.send_edit("404: directory not found . . .",text_type=["mono"], delme=4)
    else:
        await app.send_edit(
            f"`{app.Trigger()[0]}upload [file path ]` to upload to current Telegram chat",
            delme=4
        )





@app.on_message(gen(["batchup", "bcp"], exclude=["sudo"]))
async def batchupload_handler(_, m: Message):
    """ function to upload files of a directory """

    if app.textlen() > 4096:
        return await app.send_edit(
            "The message is too long. (must be less than 4096 character)",
            delme=4,
            text_type=["mono"]
        )

    if app.long() == 1:
        return await app.send_edit(
            "Give me a location to upload files from the directory . . .",
            delme=2,
            text_type=["mono"]
        )

    elif app.long() > 1:
        temp_dir = m.command[1]
        if not temp_dir.endswith("/"):
            temp_dir += "/"

    if os.path.exists(temp_dir):
        try:
            await app.send_edit(f"Uploading Files from `{temp_dir}` . . .")
            files = os.listdir(temp_dir)
            files.sort()
            for file in files:
                if (not file.endswith(".session") or
                    file in ["__pycache__", ".git", ".github", ".heroku"]):
                    c_time = time.time()
                    required_file_name = temp_dir + file
                    thumb_image_path = await app.IsThumbExists(required_file_name)
                    doc_caption = os.path.basename(required_file_name)
                    app.log.info(f"Uploading {required_file_name} from {temp_dir} to Telegram.")

                    await app.send_document(
                        chat_id=m.chat.id,
                        document=required_file_name,
                        thumb=thumb_image_path,
                        caption=doc_caption,
                        disable_notification=True,
                    )
                    await app.send_edit(f"Uploaded all files from Directory `{temp_dir}`", delme=3)
                    app.log.info("Uploaded all files in batch !!")

        except Exception as e:
            await app.error(e)
    else:
        return await app.send_edit("404: directory not found . . .", delme=2)
