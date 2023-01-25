"""
This page gives inline anime quotes.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("animequote-tab"))
async def anime_quotes_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            "`Searching quote . . .`",
            reply_markup=reply_markup
        )
        await cb.edit_message_text(
            app.animeQuote(),
            reply_markup=app.buildMarkup(
                [app.buildButton("More", "animequote-tab")]
            )
        )
    except Exception as e:
        await app.error(e)
