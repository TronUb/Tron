"""
This file gives inline results with bot having via botusername tag.
"""

from pyrogram import filters

from pyrogram.enums import ParseMode

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)

from main.userbot.client import app





# via bot messages
@app.bot.on_inline_query(filters.user(app.id))
def inline_result(_, inline_query):
    query = inline_query.query
    if query.startswith("#pmpermit"):
        inline_query.answer(
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
    elif query.startswith("#helpdex"):
        inline_query.answer(
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
                                ["• Settings •", "settings-tab"],
                                ["• Plugins •", "plugins-tab"]
                            )
                        ),
                        app.BuildKeyboard(
                            (
                                ["• Extra •", "extra-tab"],
                                ["• Stats •", "stats-tab"]
                            )
                        ),
                        app.BuildKeyboard(([["About", "about-tab"]])),
                        app.BuildKeyboard(([["Close", "close-tab"]]))
                    ]
                )
            )
            ],
        cache_time=1
        )
    elif query.startswith("#ialive"):
        inline_query.answer(
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
        inline_query.answer(
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
