"""
Inline assistant page for help menu.
"""

from pyrogram import filters
from pyrogram.types import (
    InputMediaPhoto,
    CallbackQuery
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("assistant-tab"))
@app.alert_user
async def _assistant(_, cb: CallbackQuery):
    try:
        await cb.edit_message_media(
            media=InputMediaPhoto(
                media=app.BotPic,
                caption=app.assistant_tab_string
            ),
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "home-tab")
                ]
            )
        )
    except Exception as e:
        await app.error(e)
