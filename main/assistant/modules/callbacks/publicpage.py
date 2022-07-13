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
        text=app.public_tab_string(),
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





@app.bot.on_callback_query(filters.regex("public-commands-tab"))
async def _global_commands(_, cb):
    await cb.edit_message_text(
        text=app.public_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="back-to-public"
                    )
                ]
            ]
        )
    )


@app.bot.on_callback_query(filters.regex("back-to-public"))
async def _back_to_info(_, cb):
    await cb.edit_message_text(
        text="You can use these public commands, check below.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• View commands •",
                        callback_data="public-commands-tab"
                    )
                ]
            ]
        )
    )
