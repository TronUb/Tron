"""
This file creates pages for settings in help menu.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("settings-tab"))
@app.alert_user
async def _settings(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.settings_tab_string,
        reply_markup=app.buildMarkup(
            [app.buildButton("Restart bot", "restart-tab")],
            [app.buildButton("Shutdown bot", "shutdown-tab")],
            [app.buildButton("Update bot", "update-tab")],
            [
                app.buildButton("Home", "close-tab"),
                app.buildButton("Back", "home-tab")
            ]
        )
    )
