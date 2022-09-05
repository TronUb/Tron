from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import AlreadyJoinedError

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import UserNotParticipant

from main import app, bot




public = app.VcBotAccess()

def vc_allowed(message):
    if message.from_user.is_self:
        return True

    if public:
        return True

    return None


@bot.on_message(filters.command("vcplay"))
async def vcplay_handler(_, m: Message):
    try:
        if not vc_allowed(m):
            return

        if not m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            return await bot.send_message(
                m.chat.id,
                "You can't use this command here !"
            )

        try:
            args = m.text.split(None, 1)[1]
        except IndexError:
            return await bot.send_message(
                m.chat.id,
                "Give me song name to start in vc.",
            )

        await bot.send_message(
            m.chat.id,
            f"Playing {args} . . ."
        )

        await app.get_chat_member(
            m.chat.id,
            app.id
        )

        await app.create_group_call(m.chat.id, m.id)
        data = app.Ytdl().extract_info(f"ytsearch:{args}", download=False)['entries'][0]
        url = data.get("url")

        await app.pytgcall.join_group_call(
            m.chat.id,
            AudioPiped(url)
        )
    except AlreadyJoinedError:
        await app.pytgcall.change_stream(
            m.chat.id,
            AudioPiped(url)
        )
    except UserNotParticipant:
        return await bot.send_message(
            m.chat.id,
            "The owner of this bot is not in this group, add them first !"
        )
    except Exception as e:
        await app.error(e)




@bot.on_message(filters.command("vcstop"))
async def vcstop_handler(_, m: Message):
    try:
        if not vc_allowed(m):
            return

        if not m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            return await bot.send_message(
                m.chat.id,
                "You can't use this command here !"
            )

        call_on = await app.get_group_call(m.chat.id)
        if not call_on:
            return await bot.send_message(
                m.chat.id,
                "No group call (vc) is active.",
           )

        call_discard = await app.discard_group_call(m.chat.id)
        if not call_discard:
            return await bot.send_message(
                m.chat.id,
                "Unable to stop group call (vc).",
           )
    except Exception as e:
        await app.error(e)



@bot.on_message(filters.command("vcpause"))
async def vcpause_handler(_, m: Message):
    try:
        if not vc_allowed(m):
            return

        if not m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            return await bot.send_message(
                m.chat.id,
                "You can't use this command here !"
            )
        await app.pytgcall.pause_stream(m.chat.id)
        await bot.send_message(
            m.chat.id,
            "Vc bot is paused !"
        )
    except Exception as e:
        await app.error(e)



@bot.on_message(filters.command("vcresume"))
async def vcresume_handler(_, m: Message):
    try:
        if not vc_allowed(m):
            return

        if not m.chat.type in (ChatType.SUPERGROUP, ChatType.GROUP):
            return await bot.send_message(
                m.chat.id,
                "You can't use this command here !"
            )
        await app.pytgcall.resume_stream(m.chat.id)
        await bot.send_message(
            m.chat.id,
            "Vc bot is resumed !"
        )
    except Exception as e:
        await app.error(e)
