""" Pastebin plugin """

import asyncio
from pyrogram.types import Message
from main import app


@app.on_cmd(
    commands=["paste", "bin"], usage="Paste your text in pastebin & get a link."
)
async def paste_handler(_, m: Message):
    """Paste handler for pastebin plugin"""
    reply = m.reply_to_message
    text = None

    if reply and (reply.text or reply.caption):
        text = reply.text or reply.caption
    elif not reply and len(m.command) > 1:
        text = m.text.split(None, 1)[1]

    if not text:
        return await app.send_edit(
            "Please reply to a message or provide text after the command.",
            text_type=["mono"],
            delme=4,
        )

    await app.send_edit("Pasting to pastebin . . .", text_type=["mono"])

    url = await app.HasteBinPaste(text)
    if not url:
        return await app.send_edit(
            "Failed to paste: No URL returned.", text_type=["mono"], delme=4
        )

    reply_text = f"**Pastebin** : [Click Here]({url})"

    delete = (
        True
        if len(m.command) > 1
        and m.command[1] in ["d", "del"]
        and reply
        and reply.from_user.is_self
        else False
    )

    if delete:
        await asyncio.gather(
            app.send_edit(reply_text, disable_web_page_preview=True), reply.delete()
        )
    else:
        await app.send_edit(reply_text, disable_web_page_preview=True)
