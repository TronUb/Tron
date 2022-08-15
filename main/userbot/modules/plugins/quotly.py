""" quotly plugin """

import asyncio

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"quotly" : (
        "quotly",
        {
        "q [color] [reply to message]" : "Make Stickers Of Your Texts."
        }
        )
    }
)



@app.on_message(gen(["q", "quotly"]))
async def quotly_handler(_, m: Message):
    """ quotly handler for quotly plugin """
    try:
        reply = m.reply_to_message
        if not reply:
            return await app.send_edit(m, "Reply to any users text message", delme=4)

        if app.long() > 1:
            color = m.text.split(None, 1)[1]
        else:
            color = "black"

        msg_one = await app.send_edit("Making a Quote . . .", text_type=["mono"])
        await app.send_message("QuotLyBot", f"/qcolor {color}")
        await reply.forward("QuotLyBot")
        is_sticker = True
        while is_sticker:
            try:
                msg = await app.get_last_msg(chat_id="QuotLyBot")
                if msg.sticker and msg.sticker.file_id:
                    is_sticker = False
            except Exception:
                await asyncio.sleep(0.10)
        if msg.id:
            await asyncio.gather(
                msg_one.delete(),
                app.copy_message(
                    m.chat.id,
                    "QuotLyBot",
                    msg.id
                )
            )
    except Exception as e:
        await app.error(e)
