"""
This file creates extra page tab menu in helpdex
"""

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	CallbackQuery,
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("extra-tab"))
@app.alert_user
async def _extra(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.extra_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• Public commands •",
                        callback_data="ubpublic-commands-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="home-tab"
                    )
                ]
            ]
        )
    )
