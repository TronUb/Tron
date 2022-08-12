""" broadcast plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid 

from main import app, gen




app.CMD_HELP.update(
    {"broadcast" : (
        "broadcast",
        {
        "alive" : "Broadcast messages in user chats, group chats."
        }
        )
    }
)



async def broadcast(dialog, args):
    app.send_message(
        dialog.chat.id,
        args.text.split(None, 1)[1]
    )


@app.on_message(gen(["broadcast", "bdc"]))
async def broadcast_handler(_, m: Message):
    """ broadcast handler for broadcast plugin """
    try:
        args = app.GetArgs(m)
        users = 0
        groups = 0

        if not args:
            return await app.send_edit(
                "Give me some broadcasting message.",
                text_type=["mono"],
                delme=3
            )

        try:

            async for x in app.get_dialogs():
                if x.chat.type == ChatType.PRIVATE:
                    await broadcast(x, args)
                    users += 1
                elif x.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                    await broadcast(x, args)
                    groups += 1

        except PeerIdInvalid:
            pass

        await app.send_edit(f"Broadcasted messages to {users} users & {groups} groups.", delme=4)
    except Exception as e:
        await app.error(e)
