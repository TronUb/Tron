"""
This file is for closed page inline help menu.
"""

from pyrogram import filters

from pyrogram.types import (
    InputMediaPhoto,
    CallbackQuery
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("close-tab"))
@app.alert_user
async def close_helpmenu_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_media(
            media=InputMediaPhoto(
                media="main/others/resources/images/tron-vertical.png", 
                caption=app.close_tab_string
            ),
            reply_markup=app.buildMarkup(
                [app.buildButton("Open", "home-tab")],
                [app.buildButton("Delete", "delete-tab")]
            )
        )
    except Exception as e:
        await app.error(e)
