""" pastebin plugin """

import asyncio

from pyrogram.types import Message

from main import app, gen





app.CMD_HELP.update(
    {"nekobin" : (
        "nekobin",
        {
        "bin [reply to text]" : "Paste Texts To Nekobin Site, You Can Easily Read The Texts Without Downloading The file."
        }
        )
    }
)




@app.on_message(gen(["paste", "bin"]))
async def paste_handler(_, m: Message):
    """ paste handler for pastebin plugin """
    reply = m.reply_to_message

    if reply and reply.text or reply.caption:
        text = reply.text or reply.caption
    elif not reply and app.long() > 1:
        text = m.text.split(None, 1)[1]
    elif not reply and app.long() == 1:
        return await app.send_edit(
            "Please reply to a message or give some text after command.",
            text_type=["mono"],
            delme=4
        )

    await app.send_edit("Pasting to pastebin . . .", text_type=["mono"])
    url = await app.HasteBinPaste(text)
    reply_text = f"**Hastebin** : [Click Here]({url})"
    delete = (True if app.long() > 1 and m.command[1] in ["d", "del"] and reply.from_user.is_self else False)
    if delete:
        await asyncio.gather(
            app.send_edit(
                reply_text,
                disable_web_page_preview=True
            ),
            await reply.delete()
        )
    else:
        await app.send_edit(
            reply_text,
            disable_web_page_preview=True
        )
