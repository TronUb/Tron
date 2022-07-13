"""
This file creates pages for userbot shutdown>
"""

import sys
import heroku3

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from main.userbot.client import app






@app.bot.on_callback_query(filters.regex("shutdown-tab"))
@app.alert_user
async def _shutdown_tron(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.shutdown_tab_string("`Press confirm to shutdown userbot.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-shutdown"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Home",
                        callback_data="close-tab"
                    ),
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )
    )


@app.bot.on_callback_query(filters.regex("confirm-shutdown"))
@app.alert_user
async def _shutdown_core(_, cb):
    await cb.edit_message_text(
        text=app.shutdown_tab_string("`Trying to shutdown userbot . . .`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="settings-tab"
                    )
                ]
            ]
        )
    )
    access = heroku3.from_key(app.HEROKU_API_KEY)
    application = access.apps()[app.HEROKU_APP_NAME]
    if not application:
        await cb.edit_message_text(
            text=app.shutdown_tab_string("`Failed to shutdown userbot . . .`"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Back",
                            callback_data="settings-tab"
                        )
                    ]
                ]
            )
        )
    else:
        if application:
            application.process_formation()["worker"].scale(0)
            await cb.edit_message_text(
                text=app.shutdown_tab_string("`Successfully shutdown userbot . . .`"),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data="settings-tab"
                            )
                        ]
                    ]
                )
            )
        else:
            sys.exit(0)
