import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app





@app.bot.on_callback_query(filters.regex("update-tron"))
@app.alert_user
async def _update_callback(_, cb):
	pass
