"""
This file creates stats page in help menu.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("stats-tab"))
@app.alert_user
async def stats_callback(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.stats_tab_string,
        reply_markup=app.buildMarkup(
            [app.buildButton("Refresh", "stats-tab")],
            [app.buildButton("Back", "home-tab")]
        )
    )
