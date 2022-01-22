from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup, 
	Message,
)

from tronx import app





settings = app.build_keyboard((["• Settings •", "open-settings-dex"], ["• Modules •", "tron-dex-2"]))
extra = app.build_keyboard((["• Extra •", "open-extra-dex"], ["• Stats •", "open-stats-dex"]))
about = app.build_keyboard(([["About", "open-about-dex"]]))
close = app.build_keyboard(([["Close", "close-dex"]]))
approve = app.build_keyboard(([["Approve", "approve-user"]]))
global_command = app.build_keyboard(([["• Global commands •", "global-commands"]]))
home_back = app.build_keyboard((["Home", "close-dex"], ["Back", "open-start-dex"]))





# /start command for bot
@app.bot.on_message(filters.command("help"))
async def start(_, m: Message):
	if m.from_user:
		if m.from_user.id == app.USER_ID:
			# bot pic
			if app.BotPic().endswith(".jpg" or "png" or "jpeg"):
				info = await app.bot.send_photo(
					m.chat.id,
					app.BotPic(),
					app.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			elif app.BotPic().endswith(".mp4" or ".gif"):
				info = await app.bot.send_photo(
					m.chat.id,
					app.BotPic(),
					app.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			else:
				info = await app.bot.send_message(
					m.chat.id,
					app.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
					[ settings, extra, about, close ]
					),
				)

		elif m.from_user.id != USER_ID:
			info = await app.bot.send_photo(
				m.chat.id,
				app.PIC,
				f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
				reply_markup=InlineKeyboardMarkup(
					[global_command]
				),
			)
		app.message_ids.update({info.chat.id : info.message_id})
	else:
		return




