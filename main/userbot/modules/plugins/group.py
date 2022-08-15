""" group plugin """

import asyncio

from pyrogram.raw import functions
from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"group" : (
        "group",
        {
        "bgroup [group name]" : "Creates a basic group.",
        "sgroup [group name]" : "Creates a super group.",
        "unread" : "Mark a chat as unread in your telegram folders.",
        "channel [channel name]" : "Create a channel through this command."
        }
        )
    }
)




@app.on_message(gen(["bgroup", "bgp"], exclude =["sudo"]))
async def basicgroup_handler(_, m: Message):
    """ basic group handler for group plugin """
    grpname = None
    users = None
    if app.long() == 1:
        return await app.send_edit(f"Usage: `{app.PREFIX}bgroup mygroupname`", delme=4)
    elif app.long() > 1:
        grpname = m.text.split(None, 1)[1]
        users = "@TheRealPhoenixBot"
    elif app.long() > 2:
        grpname = m.text.split(None, 1)[1]
        users = m.text.split(None, 2)[2].split()
    else:
        grpname = False
        users = "@TheRealPhoenixBot" # required

    try:
        if grpname:
            await app.send_edit(f"Creating a new basic group: `{grpname}`")
            group = await app.create_group(title=f"{grpname}", users=users)
            await app.send_edit(
                f"**Created a new basic group:** [{grpname}]({(await app.get_chat(group.id)).invite_link})"
                )
        else:
            await app.send_edit("No group name is provided.", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(gen(["sgroup", "sgp"], exclude =["sudo"]))
async def supergroup_handler(_, m: Message):
    """ super group handler for group plugin """
    grpname = None
    about = None
    if app.long() == 1:
        return await app.send_edit(f"`Usage: {app.PREFIX}sgroup mygroupname`", delme=4)
    elif app.long() > 1:
        grpname = m.text.split(None, 1)[1]
        about = ""
    elif app.long() > 2:
        grpname = m.text.split(None, 1)[1]
        about = m.text.split(None, 2)[2]
    else:
        grpname = False
        about = ""

    try:
        if grpname:
            await app.send_edit(f"Creating a new super group: `{grpname}`")
            group = await app.create_supergroup(title=f"{grpname}", description=about)
            await app.send_edit(
                f"**Created a new super group:** [{grpname}]({(await app.get_chat(group.id)).invite_link})"
            )
        else:
            await app.send_edit("No group name is provided.", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)




@app.on_message(gen(["unread", "un"], exclude =["sudo"]))
async def unreadchat_handler(_, m: Message):
    """ unread chat handler for group plugin """
    try:
        await asyncio.gather(
            m.delete(),
            app.invoke(
                functions.messages.MarkDialogUnread(
                    peer=await app.resolve_peer(m.chat.id),
                    unread=True
                )
            ),
        )
    except Exception as e:
        await app.error(e)




@app.on_message(gen("channel", exclude =["sudo"]))
async def channel_handler(_, m: Message):
    """ channel handler for group plugin """
    chname = None
    about = None
    if app.long() == 1:
        return await app.send_edit(f"Usage: `{app.PREFIX}channel [channel name]`", delme=4)

    elif app.long() > 1:
        chname = m.text.split(None, 1)[1]
        about = ""
    elif app.long() > 2:
        chname = m.text.split(None, 1)[1]
        about = m.text.split(None, 2)[2]

    try:
        if chname:
            await app.send_edit(f"Creating your channel: `{chname}`")
            response = await app.create_channel(title=f"{chname}", description=about)
            if response:
                await app.send_edit(
                    f"**Created a new channel:** [{chname}]({(await app.get_chat(response.id)).invite_link})",
                    disable_web_page_preview=True
                )
            else:
                await app.send_edit("Couldn't create a channel.")
    except Exception as e:
        await app.error(e)
