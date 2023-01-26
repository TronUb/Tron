"""
This file creates extra page tab menu in helpdex
"""

from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InputMediaPhoto
)

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("extra-tab"))
@app.alert_user
async def extra_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_media(
            media=InputMediaPhoto(
                    media=app.BotPic,
                    caption=app.extra_tab_string
            ),
            reply_markup=app.buildMarkup(
                [app.buildButton("• Public commands •", "ubpublic-commands-tab")],
                [app.buildButton("Counter", "counter-tab")],
                [app.buildButton("Calculator", "calculator-tab")],
                [app.buildButton("My Groups", "mygroups-tab")],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "home-tab")
                ]
            )
        )
        print(cb)
    except Exception as e:
        await app.error(e)
