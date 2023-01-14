"""
This file creates global commands for public users.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("ubpublic-commands-tab"))
@app.alert_user
async def ubpublic_commands_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text=app.public_tab_string,
            reply_markup=app.buildMarkup(
                [app.buildButton("Back", "extra-tab")]
            )
        )
    except Exception as e:
        await app.error(e)



@app.bot.on_callback_query(filters.regex(r"public-commands-tab(.[a-z]+)?"))
async def public_commands_callback(_, cb):
    try:
        if cb.matches[0].group(0) == "public-commands-tab-back":
            text = "You can use these public commands, check below."
            keyboard_text = "• View commands •"
            keyboard_callback_data = "public-commands-tab"
        else:
            text = app.public_tab_string
            keyboard_text = "Back"
            keyboard_callback_data = "public-commands-tab-back"
    
        await cb.edit_message_text(
            text=text,
            reply_markup=app.buildMarkup(
                [app.buildButton(text, callback_data)]
            )
        )
    except Exception as e:
        await app.error(e)
