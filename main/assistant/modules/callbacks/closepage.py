"""
This file is for closed page inline help menu.
"""

from pyrogram import filters

from pyrogram.types import (
	InputMediaPhoto,
	InlineKeyboardMarkup,
	CallbackQuery
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("close-tab"))
@app.alert_user
async def _close(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(
            media="https://raw.githubusercontent.com/TronUb/Tron/beta/main/core/resources/images/tron-vertical.png", 
            caption=app.close_tab_string()
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open",
                        callback_data="home-tab"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Delete",
                        callback_data="delete-tab"
                    )
                ]
            ]
        )
    )
