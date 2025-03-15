from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden, RPCError

from main import app
from main.core.enums import UserType


async def broadcast(dialog, text):
    try:
        return await app.send_message(
            dialog.chat.id,
            text,
            disable_web_page_preview=True,  # Prevent preview issues
            parse_mode="Markdown",  # Use Markdown formatting
        )
    except ChatWriteForbidden:
        return None  # Bot cannot write in this chat
    except RPCError as e:
        print(f"Failed to send message to {dialog.chat.id}: {e}")
        return None


@app.on_cmd(
    commands=["broadcast", "bdt"],
    usage="Broadcast messages in groups/user chats.",
    disable_for=UserType.SUDO
)
async def broadcast_handler(_, m: Message):
    try:
        args = app.GetArgs()

        if not args:
            return await app.send_edit(
                "Please provide a message to broadcast.", text_type=["mono"], delme=3
            )

        text = " ".join(args)  # Fixing argument extraction

        users = 0
        groups = 0

        await app.send_edit("Broadcasting messages . . .", text_type=["mono"])

        async for x in app.get_dialogs():
            if x.chat.type in (ChatType.PRIVATE, ChatType.SUPERGROUP, ChatType.GROUP):
                done = await broadcast(x, text)
                if done:
                    if x.chat.type == ChatType.PRIVATE:
                        users += 1
                    else:
                        groups += 1

        await app.send_edit(f"Broadcasted messages to {users} users & {groups} groups.", delme=4)

    except Exception as e:
        await app.error(f"Broadcast failed: {e}")
