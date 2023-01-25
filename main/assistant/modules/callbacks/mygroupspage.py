"""
This file creates pages for settings in help menu.
"""

from pyrogram import filters, enums
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("mygroups-tab"))
@app.alert_user
async def mygroups_callback(_, cb: CallbackQuery):
    try:
        buttons = [
            [app.buildButton(x.chat.title, x.chat.id)] async for x in 
            app.get_dialogs() if x.chat.type == enums.ChatType.SUPERGROUP and 
            x.chat.is_creator
        ]
        await cb.edit_message_text(
            text="Available Groups That Belong To You.",
            reply_markup=app.buildMarkup(*buttons)
        )
    except Exception as e:
        await app.error(e)
