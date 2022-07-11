""""
This file creates pages for updating the userbot to latet versions
"""

from pyrogram import filters

from pyrogram.types import (
    CallbackQuery
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("update-tab"))
@app.alert_user
async def _update_callback(_, cb: CallbackQuery):
    await cb.answer(
            text="This feature is not implemented yet.",
            show_alert=True
        )
