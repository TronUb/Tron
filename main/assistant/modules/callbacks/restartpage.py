"""
This file creates userbot restarting page.
"""

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
    back_button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data="settings-tab"
                )
            ]
        ]
    )

    await cb.edit_message_text(
        text=app.restart_tab_string("`Trying to restart userbot . . .`"),
        reply_markup=back_button
    )
    if not app.heroku_app():
        await cb.edit_message_text(
            text=app.restart_tab_string("`Heroku requirements missing (heroku - key, app name), restart manually . . .`"),
            reply_markup=back_button
        )
    else:
        await cb.edit_message_text(
            text=app.restart_tab_string("`Please wait 2-3 minutes to restart userbot . . .`"),
            reply_markup=back_button
        )
