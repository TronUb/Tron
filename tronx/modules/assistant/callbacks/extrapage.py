import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app







@app.bot.on_callback_query(filters.regex("extra-tab"))
@app.alert_user
async def _extra(_, cb):
	await cb.edit_message_text(
		text="**Dex:** Extra\n\nLocation: /home/extra",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"• Public commands •",
						callback_data="public-commands-tab"
					)
				],
				[
					InlineKeyboardButton(
						"Home",
						callback_data="close-tab"
					),
					InlineKeyboardButton(
						"Back",
						callback_data="home-tab"
					)
				],
			]
		),
	)