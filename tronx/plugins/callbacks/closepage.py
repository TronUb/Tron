import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app





@app.bot.on_callback_query(filters.regex("close-dex"))
@app.alert_user
async def _close(_, cb: CallbackQuery):
	await cb.edit_message_text(
		text=app.closed_menu_string(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"Open", callback_data="open-start-dex",
					)
				],
				[
					InlineKeyboardButton(
						"Delete", callback_data="delete-dex",
					)
				]
			]
		),
	)