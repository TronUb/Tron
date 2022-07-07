import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup, 
	InputMediaPhoto,
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot
from main.userbot.client import app



about_text = f"""
**Dex:** About

**Location:** /home/about

**[ Personal Info ]:**

**Name:** {bot.assistant_name}

**[ Versions ]:**

**Python:** {bot.python_version}
**Pyrogram:** {bot.pyrogram_version}
**Assistant:**  {bot.assistant_version}

**[ About ]:**

I am Nora made by ࿇•ẞᗴᗩSԵ•࿇.
I am your friendly assistant, 
i will help you as much as you need. 
You can ask me for any help related to your userbot. 
If you have any suggestions or you're facing any problems 
which are related to tronuserbot then just ask in [support group](https://t.me/tronuserbot_support)
"""






@bot.on_callback_query(filters.regex("about-tab"))
@app.alert_user
async def _about(_, cb):
	await cb.edit_message_media(
		media=InputMediaPhoto(media="./resources/images/nora.png", caption=about_text),
		reply_markup=InlineKeyboardMarkup([bot.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))]),
	)
