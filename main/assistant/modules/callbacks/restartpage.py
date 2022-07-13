"""
This file creates userbot restarting page.
"""

import heroku3

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from main.userbot.client import app






@app.bot.on_callback_query(filters.regex("restart-tab"))
@app.alert_user
async def _restart_tron(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.restart_tab_string("`Press confirm to restart.`"),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Confirm",
                        callback_data="confirm-restart-tab"
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
        ),
    )


@app.bot.on_callback_query(filters.regex("confirm-restart-tab"))
@app.alert_user
async def _restart_core(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text=app.restart_tab_string("`Trying to restart userbot . . .`"),
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
    restart = application.restart()
    if not restart:
        await cb.edit_message_text(
            text=app.restart_tab_string("`Failed to restart, restart manually . . .`"),
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
        await cb.edit_message_text(
            text=app.restart_tab_string("`Please wait 2-3 minutes to reboot userbot . . .`"),
                """,
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
