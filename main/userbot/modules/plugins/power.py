""" power plugin """

import os
import sys
import time
import asyncio

from pyrogram.types import Message

from main import app
from main.core.enums import UserType


@app.on_cmd(
    commands="reboot",
    usage="Reboot your userbot.",
    disable_for=UserType.SUDO
)
async def reboot_handler(_, m: Message):
    """Reboot handler for power plugin"""

    try:
        msg = await app.send_edit("Restarting bot . . .", text_type=["mono"])

        # Allow message to be visible before restarting
        await asyncio.sleep(2)

        # Restart the bot
        os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        await m.edit("Failed to restart userbot!", delme=2, text_type=["mono"])
        await app.error(e)

@app.on_cmd(
    commands="sleep",
    usage="Make your bot sleep.",
    disable_for=UserType.SUDO
)
async def sleep_handler(_, m: Message):
    """Sleep handler for power plugin"""

    if len(m.command) == 1:
        return await app.send_edit("Give me some seconds after command . . .", delme=3)

    arg = m.command[1]

    if not arg.isdigit():
        return await app.send_edit(
            "Please provide a valid number (seconds).", delme=3, text_type=["mono"]
        )

    sleep_time = int(arg)

    if sleep_time > 86400:
        return await app.send_edit(
            "Sorry, you can't sleep the bot for more than 24 hours (> 86400 seconds).",
            text_type=["mono"],
            delme=3,
        )

    # Convert time to a readable format
    if sleep_time < 60:
        suffix = f"{sleep_time} seconds"
    elif sleep_time < 3600:
        suffix = f"{sleep_time // 60} minutes"
    else:
        suffix = f"{sleep_time // 3600} hours"

    await app.send_edit(f"Sleeping for {suffix} . . .", delme=3)
    await time.sleep(sleep_time)
