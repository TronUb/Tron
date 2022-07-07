import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.userbot.client import app





@app.bot.on_callback_query(filters.regex("update-tab"))
@app.alert_user
async def _update_callback(_, cb):
	await cb.answer(
			"This feature is not implemented yet.",
			show_alert=True,
		)
