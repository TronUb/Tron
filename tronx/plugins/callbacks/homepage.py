import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app






@app.bot.on_callback_query(filters.regex("home-tab"))
@app.alert_user
async def _start(_, cb):
	await cb.edit_message_text(
		text = "**Dex:** Home\n\n**Description:** This is your helpdex use to navigate in different sub dex to information.",
		reply_markup=InlineKeyboardMarkup(
			[
                app.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"])),
                app.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"])),
                app.BuildKeyboard(([["About", "about-tab"]])),
                app.BuildKeyboard(([["Close", "close-tab"]]))
            ]
		),
	)