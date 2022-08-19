""" alive plugin """

import asyncio
from pyrogram.types import Message
from pyrogram.errors import BotInlineDisabled

from main import app, gen




app.CMD_HELP.update(
    {"alive" : (
        "alive",
        {
        "alive" : "Normal alive, in which you will get userbot status without inline buttons.",
        "ialive" : "Inline alive that contains your & your userbot status.",
        "iqt" : "Get inline quotes with a inline 'more' button."
        }
        )
    }
)




@app.on_message(
    gen(
        commands="alive"
    )
)
async def alive_handler(_, m: Message):
    """
        name::
            alive_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        alive_msg = "\n"
        if app.UserBio():
            alive_msg += f"⦿ {app.UserBio()}\n\n"
        alive_msg += f"⟜ **Owner:** {app.UserMention()}\n"
        alive_msg += f"⟜ **Tron:** `{app.userbot_version}`\n"
        alive_msg += f"⟜ **Python:** `{app.python_version}`\n"
        alive_msg += f"⟜ **Pyrogram:** `{app.pyrogram_version}`\n"
        alive_msg += f"⟜ **Uptime:** {app.uptime()}\n\n"

        pic = app.UserPic()

        if (pic) and (pic.endswith(".mp4" or ".mkv" or ".gif")):
            await m.delete()
            await app.send_video(
                m.chat.id,
                pic,
                caption=alive_msg
                )
        elif (pic) and (pic.endswith(".jpg" or ".jpeg" or ".png")):
            await m.delete()
            await app.send_photo(
                m.chat.id,
                pic,
                caption=alive_msg
                )
        elif not pic:
            await app.send_edit(
                alive_msg,
                disable_web_page_preview=True,
                )
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands="ialive"
    )
)
async def inlinealive_handler(_, m: Message):
    """
        name::
            inlinealive_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        try:
            result = await app.get_inline_bot_results(app.bot.username, "#ialive")
        except BotInlineDisabled:
            await app.send_edit("Turning inline mode to on, wait . . .", text_type=["mono"])
            await app.toggle_inline()
            result = await app.get_inline_bot_results(app.bot.username, "#ialive")

        if result:
            await app.send_inline_bot_result(
                m.chat.id,
                query_id=result.query_id,
                result_id=result.results[0].id,
                disable_notification=True,
            )
            await m.delete()
        else:
            await app.send_edit("Something went wrong, please try again later . . .", delme=2)
    except Exception as e:
        await app.error(e)




@app.on_message(
    gen(
        commands=["iquote", "iqt"]
    )
)
async def inlinequote_handler(_, m: Message):
    """
        name::
            inlinequote_handler

        parameters::
            client (pyrogram.Client): pyrogram client
            message (pyrogram.types.Message): pyrogram message

        returns::
            None
    """
    try:
        try:
            result = await app.get_inline_bot_results(app.bot.username, "#quote")
        except BotInlineDisabled:
            await app.send_edit(
                "Inline mode off. Turning inline mode on, wait . . .",
                text_type=["mono"]
            )
            await asyncio.sleep(1)
            await app.toggle_inline()
            result = await app.get_inline_bot_results(app.bot.username, "#quote")

        if result:
            await app.send_inline_bot_result(
                m.chat.id,
                query_id=result.query_id,
                result_id=result.results[0].id,
                disable_notification=True,
                )
            await m.delete()
        else:
            await app.send_edit("Please try again later !", delme=2, text_type=["mono"])
    except Exception as e:
        await app.error(e)

