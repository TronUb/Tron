# pylint: disable=W0703, C0103

""" afk module """

import time

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler

from main import app, gen





app.CMD_HELP.update(
    {"afk": (
        "afk",
        {
        "afk" : "away from keyboard, use `#afk` for important talk."
        }
        )
    }
)



handlers = []



@app.on_message(
    gen(
        commands="afk",
        exclude=["sudo"]
    ),
    group=0
)
async def afk_handler(_, m: Message):
    """
        name::
            offline_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        start = int(time.time())
        if app.long() >= 2:
            reason = m.text.split(None, 1)[1]
            app.set_afk(True, reason, start) # with reason
            add_afkhandler()
            await app.send_edit(f"{app.UserMention()} is now Offline.\nBecause: {reason}", delme=3)

        elif app.long() == 1 and app.long() < 4096:
            reason = app.AfkText()

            if reason:
                app.set_afk(True, reason, start) # with reason
                add_afkhandler()
                await app.send_edit(
                    f"{app.UserMention()} is now offline.\nBecause: {reason}",
                    delme=3
                )
            else:
                app.set_afk(True, "", start) # without reason
                add_afkhandler()
                await app.send_edit(f"{app.UserMention()} is now offline.", delme=3)

    except Exception as e:
        await app.error(e)



# notify mentioned users
async def offlinemention_handler(_, m: Message):
    """
        name::
            offlinemention_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        get = app.get_afk()
        if get and get["afk"]:
            if "-" in str(m.chat.id):
                cid = str(m.chat.id)[4:]
            else:
                cid = str(m.chat.id)

            end = int(time.time())
            otime = app.GetReadableTime(end - get["afktime"])
            if get["reason"] and get["afktime"]:
                await app.send_message(
                    m.chat.id,
                    f"Sorry {app.UserMention()} is currently offline !\n**Time:** {otime}\n**Because:** {get['reason']}",
                    reply_to_message_id=m.id
                    )
                await app.delete_message(3)
            elif get["afktime"] and not get["reason"]:
                await app.send_message(
                    m.chat.id,
                    f"Sorry {app.UserMention()} is currently offline !\n**Time:** {otime}",
                    reply_to_message_id=m.id
                    )
                await app.delete_message(3)

            text = m.text if m.text else ""
            cid = m.chat.id if m.chat and m.chat.id else 0

            await app.send_message(
                app.LOG_CHAT,
                f"""#mention\n\n
                **User:** `{m.from_user.first_name}`\n
                **Id:** {m.from_user.id}\n
                **Group:** `{m.chat.title}`\n
                **Message:** `{text[:4096]}`\n
                [Go to message](https://t.me/c/{cid}/{m.id})
                """
                )
    except Exception as e:
        await app.error(e)




async def unafk_handler(_, m: Message):
    """
        name::
            unafk_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        # don't break afk while using afk command
        commands = [f"{x}afk" for x in app.Trigger()]
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
                f"{app.UserMention()} is now online !\n**Offline Time:** `{afk_time}`"
            )
            app.set_afk(False, "", 0)
            remove_afkhandler()
            handlers.clear()

    except Exception as e:
        await app.error(e)





def add_afkhandler():
    """
        name::
            add_afkhandler

        parameters::
            None

        returns::
            None
    """
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


def remove_afkhandler():
    """
        name::
            remove_afkhandler

        parameters::
            None

        returns::
            None
    """
    try:
        app.remove_handler(*handlers[0])
        app.remove_handler(*handlers[1])
    except IndexError:
        pass
