""" broadcast plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid 

from main import app, gen




app.CMD_HELP.update(
    {"broadcast" : (
        "broadcast",
        {
        "broadcast" : "Broadcast messages in user chats, group chats."
        }
        )
    }
)



async def broadcast(dialog, text):
    await app.send_message(
        dialog.chat.id,
        text
    )


@app.on_message(gen(["broadcast", "bdc"]))
async def broadcast_handler(_, m: Message):
    """ broadcast handler for broadcast plugin """
    try:
        args = app.GetArgs()
        users = 0
        groups = 0
        text = args.text.split(None, 1)[1]

        if not args:
            return await app.send_edit(
                "Give me some broadcasting message.",
                text_type=["mono"],
                delme=3
            )

        try:

            await app.send_edit("Broadcasting messages . . .", text_type=["mono"])
            async for x in app.get_dialogs():
                if x.chat.type == ChatType.PRIVATE:
                    await broadcast(x, text)
                    users += 1
                elif x.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
                    await broadcast(x, text)
                    groups += 1

        except PeerIdInvalid:
            pass

        await app.send_edit(f"Broadcasted messages to {users} users & {groups} groups.", delme=4)
    except Exception as e:
        await app.error(e)
