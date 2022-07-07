import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot





@bot.on_callback_query(filters.regex("animequote-tab"))
async def _more_anime_quotes(_, cb):
	await cb.edit_message_text(
		bot.quote(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"More", 
						callback_data="animequote-tab",
					),
				]
			]
		),
	)