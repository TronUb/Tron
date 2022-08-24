"""
This file gives inline results with bot having via botusername tag.
"""

import re
from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)

from main.userbot.client import app




async def create_articles():
    cmds = []
    info = app.CMD_HELP

    for x in sorted([info.get(x) for x in info]):
        cmds.append(
            InlineQueryResultArticle(
                title=x[0],
                input_message_content=InputTextMessageContent(
                    "".join(await app.PluginData(x[0]))
                )
            )
        )
    return cmds




# via bot messages
@app.bot.on_inline_query(filters.user(app.id))
async def inline_result(_, inline_query):
    query = inline_query.query
    if query.startswith("#pmpermit"):
        await inline_query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url=app.PmpermitPic(),
                title="Tron Inline security system",
                description="Get tron security system inline menu.",
                caption=app.PmpermitText(),
                parse_mode=ParseMode.DEFAULT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        app.BuildKeyboard(([["Approve", "approve-tab"]]))
                    ]
                )
            )
        ],
        cache_time=1
        )
    elif query.startswith("#helpmenu"):
        emoji = app.HelpEmoji() or "•"

        await inline_query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url=app.BotPic(),
                title="Tron Inline helpdex menu",
                description="Get your inline helpdex menu.",
                caption=app.home_tab_string(),
                reply_markup=InlineKeyboardMarkup(
                    [
                        app.BuildKeyboard(
                            (
                                [f"{emoji} Settings {emoji}", "settings-tab"],
                                [f"{emoji} Plugins {emoji}", "plugins-tab"]
                            )
                        ),
                        app.BuildKeyboard(
                            (
                                [f"{emoji} Extra {emoji}", "extra-tab"],
                                [f"{emoji} Stats {emoji}", "stats-tab"]
                            )
                        ),
                        app.BuildKeyboard(([["Assistant", "assistant-tab"]])),
                        app.BuildKeyboard(([["Close", "close-tab"]]))
                    ]
                )
            )
        ],
        cache_time=1
        )
    elif query.startswith("#ialive"):
        await inline_query.answer(
        results=[
            InlineQueryResultPhoto(
                photo_url=app.ialive_pic(),
                title="Tron Inline alive",
                description="Get your inline alive results with buttons.",
                caption=app.ialive_tab_string(),
                reply_markup=InlineKeyboardMarkup(
                    [
                        app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))
                    ]
                )
            )
            ],
        cache_time=1
        )
    elif query.startswith("#quote"):
        await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Tron Inline anime quotes",
                input_message_content=InputTextMessageContent(app.quote()),
                description="Get infinite anime character quotes through this inline loop button.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "More", callback_data="animequote-tab"
                            )
                        ],
                    ]
                )
            )
        ],
        cache_time=1
        )
    elif re.match(r"(@[\w]+|[\d]+) \| (.+)", query):
        text = None
        user = None
        user_id = None

        if not "|" in query:
            return
        else:
            text = query.split("|")

        try:
            user = await app.bot.get_users(text[0])
        except PeerIdInvalid:
            return

        user_id = user.id

        old = app.bot.whisper_ids.get(str(user_id))
        if old:
            number = str(int(sorted(old)[-1])+1) # last updated msg number
        else:
            number = str(0)

        await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="whisper message.",
                input_message_content=InputTextMessageContent(f"🔒 A whisper message to {text[0]}, Only he/she can open it."),
                description="send a whisper message to someone.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="show message 🔐", 
                                callback_data=f"{app.id}|{user_id}|{number}"
                            )
                        ],
                    ]
                )
            )
        ],
        cache_time=1
        )

        # update values when results are sent
        if int(number) > 0:
             old.update({number:text[1]}) # new message
        else:
            app.bot.whisper_ids.update({str(user_id):{number:text[1]}}) # first message

        async def whisper_callback(client, cb):
                    try:
                        ids = cb.data.split("|")
                        if str(cb.from_user.id) in ids:
                            whisper_msg = client.whisper_ids.get(ids[1])
                            if whisper_msg:
                                num = whisper_msg.get(ids[2])
                            else:
                                num = None

                            if num:
                                await cb.answer(num, show_alert=True)
                                return True
                            else:
                                await cb.answer("whipser message expired.", show_alert=True)
                                return True

                        else:
                            await cb.answer("You're not allowed to view this message", show_alert=True)
                    except Exception as e:
                        print(e)

        return app.bot.add_handler(CallbackQueryHandler(callback=whisper_callback, filters=filters.regex(r"\d+[|]\d+[|]\d+")))

    else:
        await inline_query.answer(
            results=await create_articles(),
            cache_time=1
        )
