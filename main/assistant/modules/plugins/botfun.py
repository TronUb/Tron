"""
This file stores all the fun activity functions.
"""

from main.userbot.client import app

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message





collect = {}

numbers = [f"{x}" for x in range(1, 10)]
cmd_handlers = ["+", "-"]



@app.bot.on_message(filters.command(numbers, cmd_handlers) & filters.group, group=1)
async def increment_decrement(_, m: Message):
    try:
        reply = m.reply_to_message
        if not m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            return

        if reply and (reply.from_user.is_self) or (reply.from_user.is_bot):
            return

        if reply:
            prefix = [x for x in m.text]
            if str(reply.from_user.id) in collect:
                if prefix[0] == "+":
                    data = collect.get(str(reply.from_user.id))
                    collect.update({str(reply.from_user.id) : str(int(data) + int(prefix[1]))})
                    await app.bot.send_message(
                        m.chat.id,
                        f"{reply.from_user.first_name}: " + str(int(data) + int(prefix[1])) + " increments"
                    )
                elif prefix[0] == "-":
                    data = collect.get(str(reply.from_user.id))
                    collect.update({str(reply.from_user.id) : str(int(data) - int(prefix[1]))})
                    await app.bot.send_message(
                        m.chat.id,
                        f"{reply.from_user.first_name}: " + str(int(data) - int(prefix[1])) + " increments"
                    )
            else:
                if prefix[0] == "+":
                    data = {str(reply.from_user.id) : str(1)}
                    collect.update(data)
                    await app.bot.send_message(
                        m.chat.id,
                        f"{reply.from_user.first_name}: 1 increments"
                    )
                elif prefix[0] == "-":
                    data = {str(reply.from_user.id) : str(-1)}
                    collect.update(data)
                    await app.bot.send_message(
                        m.chat.id,
                        f"{reply.from_user.first_name}: 1 increments"
                    )
    except Exception as e:
        await app.error(e)
