"""
This file creates pages for userbot shutdown>
"""

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
    back_button=InlineKeyboardMarkup(
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
        text=app.shutdown_tab_string("`Trying to shutdown userbot . . .`"),
        reply_markup=back_button
    )

    if not app.heroku_app():
        await cb.edit_message_text(
            text=app.shutdown_tab_string("`Failed to shutdown userbot . . .`"),
            reply_markup=back_button
        )
    else:
        res = app.heroku_app().process_formation()["worker"].scale(0)
        process = "Successfully" if res else "Unsuccessfully"
        await cb.edit_message_text(
            text=app.shutdown_tab_string(f"`Shutdown {process} . . .`"),
            reply_markup=back_button
        )
