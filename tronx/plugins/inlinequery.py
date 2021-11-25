import time
import heroku3
import requests

from sys import (
	version_info, 
	platform,
)

from pyrogram import (
	Client, 
	filters, 
	__version__ as __pyro_version__,
)

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	InlineQueryResultArticle, 
	InlineQueryResultPhoto, 
	InputTextMessageContent, 
	CallbackQuery, 
	Message,
)

try:
	from tronx import bot
except ImportError:
	bot = None

from tronx import (
	app, 
	CMD_HELP, 
	version, 
	USER_ID, 
	USER_NAME, 
	USER_USERNAME, 
	Config,
	uptime,
	PREFIX,
	__python_version__,
	db_status,
	lara_version,
)

from tronx.helpers import (
	helpdex,
	build_keyboard,
	quote,
	data,
	ialive_pic,
	bot_bio,
	bot_pic,
)

from tronx.database.postgres import pmpermit_sql as db
from tronx.database.postgres import dv_sql as dv
from tronx.variable import message_ids



# variables
USER_ID = [USER_ID]

PIC = "https://telegra.ph/file/38eec8a079706b8c19eae.mp4"




# via bot messages
@bot.on_inline_query(filters.user(USER_ID))
def inline_res(_, inline_query):
	query = inline_query.query
	if query.startswith("#p0e3r4m8i8t5"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=Config.PMPERMIT_PIC,
				title="Tron security system",
				description="This is tron security system, leaves no spammer.",
				caption=Config.PMPERMIT_TEXT,
				parse_mode="markdown",
				reply_markup=InlineKeyboardMarkup(
					[approve]
				)
			)
			],
		cache_time=1
		)
	elif query.startswith("#t5r4o9nn6"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=Config.BOT_PIC,
				title="Installation",
				description="tron helpdex",
				caption="**Dex:** Home\n\n**Description:** This is your helpdex use to navigate in different sub dex to information.",
				parse_mode="markdown",
				reply_markup=InlineKeyboardMarkup(
					[settings, extra, about, close]
				)
			)
			],
		cache_time=1
		)
	elif query.startswith("#i2l8v3"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=ialive_pic(),
				title="Ialive query",
				description="Tron helpdex",
				caption=f"⛊  Inline Status:\n\n**⟐** {Config.USER_BIO}\n\n**⟜ Owner**: [{USER_NAME}](https://t.me/{USER_USERNAME})\n**⟜ Tron:** `{version}`\n**⟜ Python:** `{__python_version__}`\n⟜ **Pyrogram:** `{__pyro_version__}`\n⟜ **uptime:** `{uptime()}\n\n",
				parse_mode="markdown",
				reply_markup=InlineKeyboardMarkup([home_back])
			)
			],
		cache_time=1
		)
	elif query.startswith("#q7o5e"):
		inline_query.answer(
		results=[
			InlineQueryResultArticle(
				title="Inline quotes",
				input_message_content=InputTextMessageContent(
					quote()
					),
				description="inline quotes plugin command",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								"More", callback_data="more-anime-quotes"
							)
						],
					]
				)
			)
		],
	cache_time=1
	)
	print(inline_query)






