from pytgcalls.types import AudioPiped
from pyrogram import filters

from main import app, bot




@bot.on_message(filters.command("play") & filters.user(app.id))
async def vcplay_handler(_, m):
    try:
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
    except Exception as e:
        await app.error(e)
