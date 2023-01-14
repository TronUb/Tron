"""
This file creates pages for userbot shutdown>
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("shutdown-tab(.[a-z]+)?"))
@app.alert_user
async def shutdown_callback(_, cb: CallbackQuery):
    if not app.herokuApp:
        return await cb.answer(
            "Sorry you are not on Heroku Platform.",
            show_alert=True
        )

    if cb.matches[0].group(0) == "shutdown-tab-confirm":
        back_button = app.buildMarkup(
            [app.buildButton("Back", "settings-tab")]
        )

        await cb.edit_message_text(
            text=app.shutdown_tab_string("`Trying to shutdown userbot . . .`"),
            reply_markup=back_button
        )

        r = app.herokuApp.process_formation()["worker"].scale(0)
        process = "Successfully" if r else "Unsuccessfully"
        await cb.edit_message_text(
            text=app.shutdown_tab_string(f"`Shutdown {process} . . .`"),
            reply_markup=back_button
        )
    else:
        await cb.edit_message_text(
            text=app.shutdown_tab_string("`Press confirm to shutdown userbot.`"),
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Confirm", "shutdown-tab-confirm")
                ],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "settings-tab")
                ]
            )
        )
