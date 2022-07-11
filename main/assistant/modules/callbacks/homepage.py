""".
This file creates home page of helpmenu.
"""

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    CallbackQuery,
)

from main.userbot.client import app




HOMEPAGE_TEXT = """
**Dex:** Home

**Description:** This is your helpdex use to navigate in different sub dex to information.
"""






@app.bot.on_callback_query(filters.regex("home-tab"))
@app.alert_user
async def _start(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(media=app.BotPic(), caption=HOMEPAGE_TEXT),
        reply_markup=InlineKeyboardMarkup([
                app.BuildKeyboard(
                    (
                        ["• Settings •", "settings-tab"],
                        ["• Modules •", "modules-tab"]
                    )
                ),
                app.BuildKeyboard(
                    (
                        ["• Extra •", "extra-tab"],
                        ["• Stats •", "stats-tab"]
                    )
                ),
                app.BuildKeyboard(([["About", "about-tab"]])),
                app.BuildKeyboard(([["Close", "close-tab"]]))
        ]
        ),
    )
