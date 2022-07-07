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





@bot.on_callback_query(filters.regex("stats-tab"))
@app.alert_user
async def _stats(_, cb):
	await cb.edit_message_text(
		text=bot.stat_string(),
		reply_markup=InlineKeyboardMarkup([app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))]),
	)