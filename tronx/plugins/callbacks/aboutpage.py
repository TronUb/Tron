import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app





@app.bot.on_callback_query(filters.regex("about-tab"))
@app.alert_user
async def _about(_, cb):
	await cb.edit_message_text(
		text=f"**Dex:** About\n\n**Location:** /home/about\n\n**[ Personal Info ]:**\n\n**Age:** {app.assistant_age}\n**Name:** {app.assistant_name}\n**Gender:** {app.assistant_gender}\n\n**[ Versions ]:**\n\n**Python:** {app.python_version}\n**Pyrogram:** {app.pyrogram_version}\n**Assistant:**  {app.assistant_version}\n\n**[ About ]:**\n\nI am Nora made by ࿇•ẞᗴᗩSԵ•࿇\nI am your friendly assistant, i will help you as much as you need. You can ask me for any help related to your userbot. If you have any suggestions or you're facing any problems which are related to tronuserbot then just ask in [support group](https://t.me/tronuserbot_support), ",
		reply_markup=InlineKeyboardMarkup([app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))]),
	)