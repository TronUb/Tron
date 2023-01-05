"""
This page gives inline anime quotes.
"""

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	CallbackQuery
)

from main.userbot.client import app




reply_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="More",
                callback_data="animequote-tab",
            )
        ]
    ]
)

@app.bot.on_callback_query(filters.regex("animequote-tab"))
async def _anime_quotes(_, cb: CallbackQuery):
    await cb.edit_message_text(
        ". . .",
        reply_markup=reply_markup
    )
    await cb.edit_message_text(
        app.quote(),
        reply_markup=reply_markup
    )
