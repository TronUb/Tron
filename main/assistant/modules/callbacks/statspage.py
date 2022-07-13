"""
This file creates stats page in help menu.
"""

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    CallbackQuery,
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("stats-tab"))
@app.alert_user
async def _stats(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.stats_tab_string(),
        reply_markup=InlineKeyboardMarkup(
            [
                app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))
            ]
        ),
    )
