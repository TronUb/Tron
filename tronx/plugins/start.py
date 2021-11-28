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

settings = build_keyboard((["• Settings •", "open-settings-dex"], ["• Modules •", "tron-dex-2"]))
extra = build_keyboard((["• Extra •", "open-extra-dex"], ["• Stats •", "open-stats-dex"]))
about = build_keyboard(([["About", "open-about-dex"]]))
close = build_keyboard(([["Close", "close-dex"]]))
approve = build_keyboard(([["Approve", "approve-user"]]))
global_command = build_keyboard(([["• Global commands •", "global-commands"]]))
home_back = build_keyboard((["Home", "close-dex"], ["Back", "open-start-dex"]))





# /start command for bot
@bot.on_message(filters.command(["start"]))
async def start(_, m: Message):
	if m.from_user:
		if m.from_user.id in USER_ID:
			# bot pic
			if bot_pic().endswith(".jpg" or "png" or "jpeg"):
				info = await bot.send_photo(
					m.chat.id,
					bot_pic(),
					bot_bio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			elif bot_pic().endswith(".mp4" or ".gif"):
				info = await bot.send_photo(
					m.chat.id,
					bot_pic(),
					bot_bio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			else:
				info = await bot.send_message(
					m.chat.id,
					bot_bio(m),
					reply_markup=InlineKeyboardMarkup(
					[ settings, extra, about, close ]
					),
				)

		elif m.from_user.id not in USER_ID:
			info = await bot.send_photo(
				m.chat.id,
				PIC,
				f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
				reply_markup=InlineKeyboardMarkup(
					[global_command]
				),
			)
		message_ids.update({info.chat.id : info.message_id})
	else:
		return




