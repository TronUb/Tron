""" power plugin """

import os
import sys
import time

from pyrogram.types import Message

from main import app, gen
from main.core.enums import UserType



@app.on_cmd(
    commands="reboot",
    usage="Reboot your userbot.",
    disable_for=UserType.SUDO
)
async def reboot_handler(_, m: Message):
    """ reboot handler for power plugin """
    try:
        msg = await app.send_edit("Restarting bot . . .", text_type=["mono"])

        os.execv(sys.executable, ['python'] + sys.argv)
        await app.edit_message_text(
            msg.chat.id,
            msg.message_id,
            "Restart completed !\nBot is alive now !"
        )
    except Exception as e:
        await m.edit("Failed to restart userbot !", delme=2, text_type=["mono"])
        await app.error(e)




@app.on_cmd(
    commands="sleep",
    usage="Make your bot sleep.",
    disable_for=UserType.SUDO
)
async def sleep_handler(_, m: Message):
    """ sleep handler for power plugin """
    if app.long() == 1:
        return await app.send_edit("Give me some seconds after command . . .")

    elif app.long() > 1:
        arg = m.command[1]

    if arg.isdigit():
        cmd = int(arg)
        if cmd > 86400:
            return await app.send_edit(
                "Sorry you can't sleep bot for more than 24 hours (> 86400 seconds) . . .",
                text_type=["mono"],
                delme=3
            )

        formats = {
            cmd<60:f"{cmd} seconds",
            cmd>=60:f"{cmd//60} minutes",
            cmd>=3600:f"{cmd//3600} hours"
            }

        suffix = "`null`"
        for x in formats: # very small loop
            if x:
                suffix = formats[x]
                break

        await app.send_edit(f"Sleeping for {suffix} . . .", delme=cmd)
        time.sleep(cmd)
    else:
        await app.send_edit("Please give me a number not text . . .", delme=3, text_type=["mono"])
