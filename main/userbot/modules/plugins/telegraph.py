""" telegraph plugin """

import os

from telegraph import upload_file

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"telegraph" : (
        "telegraph",
        {
        "tgm [reply to message | media]" : "Reply To Media To Get Links Of That Media.\nSupported Media - (jpg, jpeg, png, gif, mp4)."
        }
        )
    }
)




@app.on_message(gen(["tgm", "telegraph"]))
async def telegraph_handler(_, m:Message):
    """ telegraph handler for supertools plugin """
    reply = m.reply_to_message
    filesize = 5242880
    # if not replied
    if not reply:
        await app.send_edit("Please reply to media / text . . .", text_type=["mono"])
    # replied to text
    elif reply.text:
        if len(reply.text) <= 4096:
            await app.send_edit("⏳• Hold on . . .", text_type=["mono"])
            link = app.telegraph.create_page(
                app.name,
                html_content=reply.text
                )
            await app.send_edit(
                f"**Telegraph Link: [Press Here](https://telegra.ph/{link.get('path')})**",
                disable_web_page_preview=True
                )
        else:
            await app.send_edit("The length text exceeds 4096 characters . . .", text_type=["mono"])
    # replied to supported media
    elif reply.media:
        if (
            reply.photo and reply.photo.file_size <= filesize # png, jpg, jpeg
            or reply.video and reply.video.file_size <= filesize # mp4
            or reply.animation and reply.animation.file_size <= filesize
            or reply.sticker and reply.sticker.file_size <= filesize
            or reply.document and reply.document.file_size <= filesize # [photo, video] document
            ):
            await app.send_edit("⏳• Hold on . . .", text_type=["mono"])
            # change ext to png to use convert in link
            if reply.animation or reply.sticker:
                loc = await app.download_media(
                    reply,
                    file_name=f"{app.TEMP_DICT}telegraph.png"
                    )
            else:
                loc = await app.download_media(
                    reply
                    )
            try:
                response = upload_file(loc)
            except Exception as e:
                return await app.error(e)
            await app.send_edit(
                f"**Telegraph Link: [Press Here](https://telegra.ph{response[0]})**",
                disable_web_page_preview=True
                )
            if os.path.exists(loc):
                os.remove(loc)
        else:
            await app.send_edit(
                "Please check the file format or file size , it must be less than 5 mb . . .",
                text_type=["mono"]
            )
    else:
        # if replied to unsupported media
        await app.send_edit("Sorry, The File is not supported !", delme=2, text_type=["mono"])
