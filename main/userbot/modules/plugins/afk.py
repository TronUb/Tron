# pylint: disable=W0703, C0103

""" afk module """

import time

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from main import app
from main.core.enums import UserType



handlers = []


@app.on_cmd(
    commands="afk",
    usage="Away from keyboard.",
    disable_for=UserType.SUDO
)
async def afk_handler(_, m: Message):

    try:
        start = int(time.time())
        if app.long() >= 2:
            reason = m.text.split(None, 1)[1]
        elif app.long() == 1:
            reason = app.AfkText
        else:
            reason = ""

        app.set_afk(True, reason, start)
        add_afkhandler()
        if reason:
            reason = f"Because: {reason}"

        await app.send_edit(f"{app.UserMention} is now Offline.\n{reason}", delme=3)
    except Exception as e:
        await app.error(e)



# while you are afk
# notify the users who mention or tag you
async def offlinemention_handler(_, m: Message):
    try:
        get = app.get_afk()

        if not (get or get["afk"]):
            return None

        reason = f"**Because:** {get['reason']}" if get["reason"] else "No Reason Mentioned"

        await app.send_message(
            m.chat.id,
            f"""
            Sorry {app.UserMention} is currently offline !\n
            **Time:** {app.GetReadableTime(int(time.time()) - get["afktime"])}\n
            {reason}
            """,
            reply_to_message_id=m.id
        )

        text = m.text if m.text else "" # could be a media so

        await app.send_message(
            app.LOG_CHAT,
            f"""
            #mention\n\n
            **User:** `{m.from_user.first_name}`\n
            **Id:** `{m.from_user.id}`\n
            **Group:** `{m.chat.title}`\n
            **Message:** `{text[:4096]}`\n
            [Go to message]({m.link})
            """
        )
    except Exception as e:
        await app.error(e)




async def unafk_handler(_, m: Message):
    try:
        # don't break afk while using afk command
        commands = [f"{x}afk" for x in app.Trigger]
        if m.text:
            if m.text.split()[0] in commands:
                return
            elif "#afk" in m.text:
                return

        get = app.get_afk()
        if get and get["afk"] and filters.outgoing:
            end = int(time.time())
            afk_time = app.GetReadableTime(end - get["afktime"])
            await app.send_message(
                m.chat.id,
                f"{app.UserMention} is now online !\n**Offline Time:** `{afk_time}`"
            )
            app.set_afk(False, "", 0)
            if len(handlers) >= 2:
                remove_afkhandler()
                handlers.clear()

    except Exception as e:
        await app.error(e)




# add handlers when user goes afk
def add_afkhandler():
    handlers.append(app.add_handler(MessageHandler(
        callback=offlinemention_handler,
        filters=~filters.bot & ~filters.channel & ~filters.me & filters.private | filters.mentioned),
        1
    ))
    handlers.append(app.add_handler(MessageHandler(
        callback=unafk_handler,
        filters=filters.me & filters.text & filters.outgoing & ~filters.channel),
        2
    ))


# remove handlers when users comes out of afk
def remove_afkhandler():
    try:
        app.remove_handler(*handlers[0])
        app.remove_handler(*handlers[1])
    except IndexError:
        pass
