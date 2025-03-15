""" info plugin """

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from main import app


@app.on_cmd(
    commands="minfo",
    usage="Get media information of a telegram media."
)
async def mediainfo_handler(_, m: Message):
    """ mediainfo handler for info plugin """
    replied = m.reply_to_message
    if not replied:
        return await app.send_edit(
            "📌 Please reply to some media to get media info . . .", text_type=["mono"]
        )

    media_types = {
        "photo": replied.photo,
        "video": replied.video,
        "sticker": replied.sticker,
        "document": replied.document,
        "animation": replied.animation,
        "audio": replied.audio,
        "text": replied.text,
    }

    media_type = app.get_file_id(replied)["type"]
    pie = media_types.get(media_type)

    if not pie:
        return await app.send_edit("❌ Unsupported media type.")

    msg = f"**📂 Type:** {media_type.capitalize()}\n"

    attributes = {
        "Width": getattr(pie, "width", None),
        "Height": getattr(pie, "height", None),
        "Size": getattr(pie, "file_size", None),
        "Duration": getattr(pie, "duration", None),
        "Mime type": getattr(pie, "mime_type", None),
        "File name": getattr(pie, "file_name", None),
        "Title": getattr(pie, "title", None),
        "Performer": getattr(pie, "performer", None),
        "Emoji": getattr(pie, "emoji", None),
        "Animated": getattr(pie, "is_animated", None),
        "Set name": getattr(pie, "set_name", None),
        "Streamable": getattr(pie, "supports_streaming", None),
        "Date": getattr(pie, "date", None),
    }

    for key, value in attributes.items():
        if value is not None:
            msg += f"**{key}:** `{value}`\n"

    if replied.caption:
        msg += f"**📜 Caption:** `{replied.caption}`\n"

    await app.send_edit("**⚶ Media Information ⚶**\n\n" + msg)


@app.on_cmd(
    commands="chatinfo",
    usage="Get chat information."
)
async def chatinfo_handler(_, m: Message):
    """ chatinfo handler for info plugin """
    try:
        if len(m.command) > 1:
            chat_u = m.command[1]
            chat = await app.get_chat(chat_u)
        else:
            if m.chat.type == ChatType.PRIVATE:
                return await app.send_edit(
                    "🔒 Please use this in groups or with `.chatinfo [group username or ID]`",
                    delme=3,
                )
            chat = await app.get_chat(m.chat.id)

        poto = False
        async for x in app.get_chat_photos(chat.id):
            poto = x.file_id
            break

        await app.send_edit("Processing . . .")

        data = "**🏷️ Chat Info:**\n\n"
        data += f"**📌 Title:** `{chat.title}`\n"
        data += f"**🆔 Chat Id:** `{chat.id}`\n"
        data += f"**📡 Chat Type:** `{chat.type}`\n"
        data += f"**🌍 Dc Id:** `{chat.dc_id}`\n"
        if chat.username:
            data += f"**🔗 Username:** `@{chat.username}`\n"
        data += f"**👥 Members:** `{chat.members_count}`\n"
        data += f"**📜 Description:** `{chat.description}`\n"

        # Check if permissions exist
        if chat.permissions:
            neel = chat.permissions
            data += "**🔒 Permissions:**\n\n"
            data += f"**✉️ Send Messages:** `{getattr(neel, 'can_send_messages', 'Unknown')}`\n"
            data += f"**📷 Send Media:** `{getattr(neel, 'can_send_media_messages', 'Unknown')}`\n"
            data += f"**🌐 Web Preview:** `{getattr(neel, 'can_add_web_page_previews', 'Unknown')}`\n"
            data += (
                f"**📊 Send Polls:** `{getattr(neel, 'can_send_polls', 'Unknown')}`\n"
            )
            data += (
                f"**⚙️ Change Info:** `{getattr(neel, 'can_change_info', 'Unknown')}`\n"
            )
            data += f"**📩 Invite Users:** `{getattr(neel, 'can_invite_users', 'Unknown')}`\n"
            data += f"**📌 Pin Messages:** `{getattr(neel, 'can_pin_messages', 'Unknown')}`\n"
        else:
            data += "**⚠️ Unable to fetch chat permissions.**\n"

        buttons = None
        if chat.username:
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔗 Open Chat", url=f"https://t.me/{chat.username}"
                        )
                    ]
                ]
            )

        if poto:
            await app.send_cached_media(
                m.chat.id, file_id=poto, caption=data, reply_markup=buttons
            )
            await m.delete()
        else:
            await app.send_edit(data, reply_markup=buttons)

    except Exception as e:
        await app.error(e)
