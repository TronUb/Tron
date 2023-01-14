"""
This file creates userbot restarting page.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app






@app.bot.on_callback_query(filters.regex(r"restart-tab(.[a-z]+)?"))
@app.alert_user
async def restart_callback(_, cb: CallbackQuery):
    if not app.herokuApp:
        return await cb.answer(
            "Sorry you are not on Heroku Platform.",
            show_alert=True
        )

    if cb.matches[0].group(0) == "restart-tab-confirm":
        try:
            back_button = app.bulidMarkup(
                [app.buildButton("Back", "settings-tab")]
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
                r = app.herokuApp.restart()
                text = "`Please wait 2-3 minutes to restart userbot . . .`"
                final_text = text if r else "`Failed to restart userbot, do it manually . . .`"
                await cb.edit_message_text(
                    text=app.restart_tab_string(final_text),
                    reply_markup=back_button
                )
        except Exception as e:
            await app.error(e)
    else:
        await cb.edit_message_text(
            text=app.restart_tab_string("`Press confirm to restart.`"),
            reply_markup=app.buildMarkup(
                [app.buildButton("Confirm", "restart-tab-confirm")],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "settings-tab")
                ]
            )
        )
