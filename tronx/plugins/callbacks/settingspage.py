import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app





@app.bot.on_callback_query(filters.regex("open-settings-dex"))
@app.alert_user
async def _settings(_, cb):
	await cb.edit_message_text(
		text="**Dex:** Settings\n\n**Location:** /home/settings",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"Restart bot", callback_data="restart-tron",
					),
				],
				[
					InlineKeyboardButton(
						"Shutdown bot", callback_data="shutdown-tron",
					)
				],
				[
					InlineKeyboardButton(
						"Update bot", callback_data="update-tron",
					)
				],
				app.BuildKeyboard((["Home", "close-dex"], ["Back", "open-start-dex"])),
			]
		),
	)