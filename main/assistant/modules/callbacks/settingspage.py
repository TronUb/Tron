import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot
from main.userbot.client import app





@bot.on_callback_query(filters.regex("settings-tab"))
@app.alert_user
async def _settings(_, cb):
	await cb.edit_message_text(
		text="**Dex:** Settings\n\n**Location:** /home/settings",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"Restart bot", callback_data="restart-tab",
					),
				],
				[
					InlineKeyboardButton(
						"Shutdown bot", callback_data="shutdown-tab",
					)
				],
				[
					InlineKeyboardButton(
						"Update bot", callback_data="update-tab",
					)
				],
				bot.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"])),
			]
		),
	)