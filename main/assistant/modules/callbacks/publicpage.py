"""
This file creates global commands for public users.
"""

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("ubpublic-commands-tab"))
@app.alert_user
async def _public_commands(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.public_tab_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="extra-tab"
                    )
                ]
            ]
        )
    )




@app.bot.on_callback_query(filters.regex("public-commands-tab(.[a-z]+)?"))
async def _global_commands(_, cb):
    if cb.matches[0].match == "public-commands-tab-back":
        text = "You can use these public commands, check below."
        keyboard_text = "• View commands •"
        keyboard_callback_data = "public-commands-tab"
    else:
        text = app.public_tab_string
        keyboard_text = "Back"
        keyboard_callback_data = "public-commands-tab-back"

    await cb.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=keyboard_text,
                        callback_data=keyboard_callback_data
                    )
                ]
            ]
        )
    )
