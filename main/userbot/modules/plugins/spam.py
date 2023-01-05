""" spam plugin """

import asyncio

from pyrogram.types import Message

from main import app, gen
from main.core.enums import UserType



@app.on_cmd(
    commands="spam",
    usage="Send a message a number of times.",
    disable_for=UserType.SUDO
)
async def spam_handler(_, m: Message):
    """ spam handler for spam plugin """
    try:
        reply = m.reply_to_message
        reply_to_id = reply.id if reply else None
        cmd = m.text.split(None, 2)

        if not reply and app.long() == 1:
            await app.send_edit(
                "Reply or give me count & spam text after command.",
                text_type=["mono"],
                delme=4
            )

        elif not reply and app.long() > 1:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else 0
            spam_msg = cmd[2]
            for _ in range(times):
                await app.send_message(
                    m.chat.id,
                    spam_msg,
                    reply_to_message_id=reply_to_id
                )
                await asyncio.sleep(0.10)

        elif reply:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else 0
            spam_msg = reply.id
            for _ in range(times):
                await app.copy_message(
                    m.chat.id,
                    m.chat.id,
                    spam_msg
                )
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands="dspam",
    usage="Spam with a delay.",
    disable_for=UserType.SUDO
)
async def delayspam_handler(_, m: Message):
    """ delay spam handler for spam plugin """
    try:
        reply = m.reply_to_message
        cmd = m.command

        if app.long() < 3:
            await app.send_edit(
                f"Use like this: `{app.Trigger()[0]}dspam [count spam] [delay time in seconds] [text messages]`"
            )

        elif app.long() > 2 and not reply:
            await m.delete()
            msg = m.text.split(None, 3)
            times = int(msg[1]) if msg[1].isdigit() else None
            sec = int(msg[2]) if msg[2].isdigit() else None
            text = msg[3]
            for _ in range(times):
                await app.send_message(
                    m.chat.id,
                    text
                )
                await asyncio.sleep(sec)
        else:
            await app.send_edit("Something wrong in spam command !")
    except Exception as e:
        await app.error(e)
