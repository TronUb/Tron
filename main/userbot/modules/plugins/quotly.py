import asyncio

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"quotly" : (
        "quotly",
        {
        "q [reply to message]" : "Make Image Of Your Texts." 
        }
        )
    }
)



@app.on_message(gen(["q"], exclude = ["sudo", "channel"]))
async def quotly_handler(_, m: Message):
    reply = m.reply_to_message
    if not reply:
        return await app.send_edit(m, "Reply to any users text message", delme=4)

    await app.send_edit("Making a Quote . . .", text_type=["mono"])
    await reply.forward("@QuotLyBot")
    is_sticker = True
    while is_sticker:
        try:
            msg = await app.get_last_msg(chat_id="@QuotLyBot")
            if msg.sticker and msg.sticker.file_id:
                is_sticker = False
        except Exception:
            await asyncio.sleep(0.5)
    if msg.id:
        await asyncio.gather(
            m.delete(),
            app.copy_message(
                m.chat.id, 
                "@QuotLyBot", 
                msg.id
                )
            )
