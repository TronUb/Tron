""" purge plugin """

from datetime import datetime

from pyrogram.types import Message

from main import app, gen
from main.core.enums import UserType



@app.on_cmd(
    commands=["purge", "p"],
    usage="Delete messages from tagged message to top fown message.",
    disable_for=UserType.SUDO
)
async def purge_handler(_, m:Message):
    """ purge handler for purge plugin """
    if m.reply_to_message:
        await app.send_edit("purging . . .", text_type=["mono"])

        start = datetime.now()

        messages = await app.get_messages(
            m.chat.id,
            range(m.reply_to_message.id, m.id),
            replies=0
        )

        msg_id = []
        msg_id.clear()

        for msg in messages:
            msg_id.append(msg.id)

        await app.delete_messages(
            m.chat.id,
            msg_id
        )

        sec = (datetime.now() - start).seconds

        await app.send_edit(
            "Deleted `{}` messages in `{}` seconds.".format(len(msg_id), sec),
            text_type=["mono"],
            delme=4
        )
    else:
        await app.send_edit(
            "Reply to a message to delete all messages from tagged message to bottom message.",
            delme=4
        )




@app.on_cmd(
    commands=["purgeme", "purgme", "pgm"],
    usage="Delete number of messages, counting from recent to oldest.",
    disable_for=UserType.SUDO
)
async def purgecount_handler(_, m:Message):
    """ purge count handler for purge plugin """
    if app.long() > 1:
        target = int(m.command[1]) if m.command[1].isdigit() and m.command[1] != 0 else 1
    else:
        return await app.send_edit(
            "Give me some number after command to delete messages.",
            text_type=["mono"],
            delme=4
        )

    start = datetime.now()
    lim = target + 1  # command msg included

    await app.send_edit(f"Deleting {target} messages . . .")

    msg_id = []
    msg_id.clear()

    async for msg in app.get_chat_history(m.chat.id, limit=lim):
        msg_id.append(msg.id)

    await app.delete_messages(m.chat.id, message_ids=msg_id[0:lim])
    sec = (datetime.now() - start).seconds

    await app.send_edit(
        "Deleted `{}` messages in `{}` seconds.".format(target, sec),
        text_type=["mono"],
        delme=4
    )




@app.on_cmd(
    commands="del",
    usage="Delete a message in a chat.",
    disable_for=UserType.SUDO
)
async def del_handler(_, m: Message):
    """ del handler for purge plugin """
    reply = m.reply_to_message
    msg_ids = [m.id, reply.id] if reply else [m.id]

    try:
        await app.delete_messages(m.chat.id, msg_ids)
    except Exception as e:
        await app.error(e)
