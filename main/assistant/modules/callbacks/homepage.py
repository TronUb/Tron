import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup, 
	InputMediaPhoto,
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot



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
                app.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"])),
                app.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"])),
                app.BuildKeyboard(([["About", "about-tab"]])),
                app.BuildKeyboard(([["Close", "close-tab"]]))
		]
		),
	)
