""".
This file creates home page of helpmenu.
"""

from pyrogram import filters
from pyrogram.types import (
    InputMediaPhoto,
    CallbackQuery,
)

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("home-tab"))
@app.alert_user
async def home_page_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_media(
            media=InputMediaPhoto(media=app.BotPic, caption=app.home_tab_string),
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("• Settings •", "settings-tab"),
                    app.buildButton("• Plugins •", "plugins-tab")
                ],
                [
                    app.buildButton("• Extra •", "extra-tab"),
                    app.buildButton("• Stats •", "stats-tab")
                ],
                [app.buildButton("Assistant", "assistant-tab")],
                [app.buildButton("Close", "close-tab")]
            )
        )
    except Exception as e:
        await app.error(e)
