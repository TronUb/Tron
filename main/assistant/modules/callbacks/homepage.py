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



homepage_text = f"""
**Dex:** Home

**Description:** This is your helpdex use to navigate in different sub dex to information.
"""






@bot.on_callback_query(filters.regex("home-tab"))
@app.alert_user
async def _start(_, cb):
	await cb.edit_message_media(
		media=InputMediaPhoto(media=app.BotPic(), caption=homepage_text),
		reply_markup=InlineKeyboardMarkup([
                bot.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"])),
            	bot.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"])),
                bot.BuildKeyboard(([["About", "about-tab"]])),
                bot.BuildKeyboard(([["Close", "close-tab"]]))
		]
		),
	)
