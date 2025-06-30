"""
This file creates global commands for public users.
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery
from main.userbot.client import app


@app.bot.on_callback_query(filters.regex(r"public-commands-tab(?:-back)?"))
async def public_commands_callback(_, cb: CallbackQuery):
    try:
        pattern = cb.matches[0].group(0) if cb.matches else ""
        is_back = pattern.endswith("-back")

        if is_back:
            text = (
                "**🛠 Public Commands Panel**\n\n"
                "You're back at the main panel!\n"
                "Tap the button below to explore available features and tools 🚀"
            )
            button_text = "• View Commands •"
            callback_data = "public-commands-tab"
        else:
            text = (
                "**📖 List of Public Commands**\n\n"
                "Here are all the commands you can use as a regular user:\n\n"
                f"{app.public_tab_string}\n\n"
                "Want to go back? Tap below."
            )
            button_text = "⬅️ Back"
            callback_data = "public-commands-tab-back"

        await cb.edit_message_text(
            text=text,
            reply_markup=app.buildMarkup([app.buildButton(button_text, callback_data)]),
            disable_web_page_preview=True,
        )
    except Exception as e:
        await app.error(e)
