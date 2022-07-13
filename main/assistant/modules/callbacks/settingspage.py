"""
This file creates pages for settings in help menu.
"""

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("settings-tab"))
@app.alert_user
async def _settings(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.settings_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Restart bot", callback_data="restart-tab",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Shutdown bot", callback_data="shutdown-tab",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Update bot", callback_data="update-tab",
                    )
                ],
                app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"])),
            ]
        ),
    )
