"""
Inline about page for help menu.
"""

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup,
	InputMediaPhoto,
	CallbackQuery
)

from main.userbot.client import app




ABOUT_TEXT = f"""
**Dex:** About

**Location:** /home/about

**[ Personal Info ]:**

**Name:** {app.assistant_name}

**[ Versions ]:**

**Python:** {app.python_version}
**Pyrogram:** {app.pyrogram_version}
**Assistant:**  {app.assistant_version}

**[ About ]:**

I am Nora made by ࿇•ẞᗴᗩSԵ•࿇.
I am your friendly assistant, 
i will help you as much as you need. 
You can ask me for any help related to your userbot. 
If you have any suggestions or you're facing any problems 
which are related to tronuserbot then just ask in 
[support group](https://t.me/tronuserbot_support)
"""






@app.bot.on_callback_query(filters.regex("about-tab"))
@app.alert_user
async def _about(_, cb: CallbackQuery):
    await cb.edit_message_media(
        media=InputMediaPhoto(media="main/core/resources/images/nora.png", caption=ABOUT_TEXT),
        reply_markup=InlineKeyboardMarkup(
            [
                app.bot.BuildKeyboard(
                    (
                        ["Home", "close-tab"],
                        ["Back", "home-tab"]
                    )
                )
            ]
        )
    )
