""" info plugin """

from pyrogram.types import Message
from pyrogram.enums import ChatType
from main import app, gen




app.CMD_HELP.update(
    {"info" : (
        "info",
        {
        "minfo [reply to media]" : "Check media info including text information.",
        "chatinfo" : "Get chats information."
        }
        )
    }
)




@app.on_message(gen("minfo"))
async def mediainfo_handler(_, m: Message):
    """ mediainfo handler for info plugin """
    replied = m.reply_to_message
    if not replied:
        return await app.send_edit(
            "Please reply to some media to get media info . . .",
            text_type=["mono"]
        )

    if (app.get_file_id(replied))["type"] == "photo":
        pie = replied.photo
        msg = "**Type:** Photo\n"
        msg += f"**Width:** `{pie.width}`\n"
        msg += f"**Height:** `{pie.height}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg += " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "video":
        pie = replied.video
        msg = "**Types:** Video\n"
        msg += f"**Width:** `{pie.width}`\n"
        msg += f"**Height:** `{pie.height}`\n"
        msg += f"**Duration:** `{pie.duration}`\n"
        msg += f"**Mime type:** `{pie.mime_type}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Streamable:** `{pie.supports_streaming}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg +=  " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "sticker":
        pie = replied.sticker
        msg = "**Types:** sticker\n"
        msg += f"**File name:** `{pie.file_name}`\n"
        msg += f"**Width:** `{pie.width}`\n"
        msg += f"**Height:** `{pie.height}`\n"
        msg += f"**Mime type:** `{pie.mime_type}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Emoji:** `{pie.emoji}`\n"
        msg += f"**Animated:** `{pie.is_animated}`\n"
        msg += f"**Set name:** `{pie.set_name}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg +=  " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "document":
        pie = replied.document
        msg = "**Types:** Document\n"
        msg += f"**File name:** `{pie.file_name}`\n"
        msg += f"**Mime type:** `{pie.mime_type}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg +=  " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "animation":
        pie = replied.animation
        msg = "**Types:** Animation\n"
        msg += f"**File name:** `{pie.file_name}`\n"
        msg += f"**Width:** `{pie.width}`\n"
        msg += f"**Height:** `{pie.height}`\n"
        msg += f"**Duration:** `{pie.duration}`\n"
        msg += f"**Mime type:** `{pie.mime_type}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg +=  " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "audio":
        pie = replied.audio
        msg = "**Types:** Audio\n"
        msg += f"**Title:** `{pie.title}`\n"
        msg += f"**Performer:** `{pie.performer}`\n"
        msg += f"**File name:** `{pie.file_name}`\n"
        msg += f"**Duration:** `{pie.duration}`\n"
        msg += f"**Mime type:** `{pie.mime_type}`\n"
        msg += f"**Size:** `{pie.file_size}`\n"
        msg += f"**Date:** `{pie.date}`\n"
        if replied.caption:
            msg += f"**Caption:** `{replied.caption}`\n"
        else:
            msg +=  " "
        await app.send_edit(
            "**⚶ Media Information ⚶**\n\n" + msg,
            )
    elif (app.get_file_id(replied))["type"] == "text":
        msg = "**Types:** Text\n"
        msg += f"**Text:** `{replied.text}`\n"
        await app.send_edit(
            "**⚶ Text Information ⚶**\n\n" + msg,
            )




@app.on_message(gen("chatinfo"))
async def chatinfo_handler(_, m: Message):
    """ chatinfo handler for info plugin """
    try:
        if app.long() > 1:
            chat_u = m.command[1]
            chat = await app.get_chat(chat_u)
        else:
            if m.chat.type == ChatType.PRIVATE:
                return await app.send_edit(
                    "Please use it in groups or use `.chatinfo [group username or id]`",
                    delme=3
                )

            else:
                chatid = m.chat.id
                chat = await app.get_chat(chatid)

        poto = False

        async for x in app.get_chat_photos(chat.id):
            poto = x.file_id
            break

        await app.send_edit("Processing . . .")
        neel = chat.permissions
        data = "**Chat Info:**\n\n"
        data += f"**Title:** `{chat.title}`\n"
        data += f"**Chat Id:** `{chat.id}`\n"
        data += f"**Chat Type:** `{chat.type}`\n"
        data += f"**Dc Id:** `{chat.dc_id}`\n"
        if chat.username:
            data += f"**Username:** `@{chat.username}`\n"
        data += f"**Members:** `{chat.members_count}`\n"
        data += f"**Description:** `{chat.description}`\n"
        data += "**Permissions:**\n\n"
        data += f"**Send Messages:** `{neel.can_send_messages}`\n"
        data += f"**Send Media:** `{neel.can_send_media_messages}`\n"
        data += f"**Web Page Preview:** `{neel.can_add_web_page_previews}`\n"
        data += f"**Send Polls:** `{neel.can_send_polls}`\n"
        data += f"**Change Group Info:** `{neel.can_change_info}`\n"
        data += f"**Invite Users:** `{neel.can_invite_users}`\n"
        data += f"**Pin Messages:** `{neel.can_pin_messages}`\n"
        if poto and data:
            await app.send_cached_media(
                m.chat.id,
                file_id=poto,
                caption=data
            )
            await m.delete()
        elif not poto:
            await app.send_edit(data)
        else:
            await app.send_edit("Failed to get information of this group . . .", delme=2)
    except Exception as e:
        await app.error(e)
