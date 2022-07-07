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





@bot.on_callback_query(filters.regex("close-tab"))
@app.alert_user
async def _close(_, cb: CallbackQuery):
	await cb.edit_message_text(
		text=bot.closed_menu_string(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"Open", callback_data="home-tab",
					)
				],
				[
					InlineKeyboardButton(
						"Delete", callback_data="delete-tab",
					)
				]
			]
		),
	)