import os
import re
import sys
import traceback
import subprocess

from io import StringIO

from pyrogram.types import Message
from pyrogram import filters

from main.userbot.client import app





@app.bot.on_message(filters.command("eval") & filters.user(app.id), group=-1)
async def bot_evaluate_handler(_, m: Message):
    """ This function is made for executing python codes """

    try:
        # double protection
        if m.from_user.id != app.id:
            return

        text = m.text
        try:
            cmd = text.split(None, 1)[1]
        except IndexError:
            cmd = None

        if not cmd:
            return await app.bot.send_message(m.chat.id, "Give me some text (code) to execute . . .")

        msg = await app.bot.send_message(m.chat.id, "Running . . .")

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await app.aexec(cmd)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        evaluation = exc or stderr or stdout or "Success"
        final_output = f"**• COMMAND:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation.strip()}`"

        if len(final_output) > 4096:
            location = await app.create_file(filename="eval_output.txt", content=str(final_output), caption=f"`{m.text}`", send=False)
            await app.bot.send_document(m.chat.id, location)
            await msg.delete()
        else:
            await msg.edit(final_output)
    except Exception as e:
        await app.error(e)
