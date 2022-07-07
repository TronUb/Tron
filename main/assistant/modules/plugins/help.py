from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup, 
	Message,
)

from main.userbot.client import app





settings = app.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"]))
extra = app.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"]))
about = app.BuildKeyboard(([["About", "about-tab"]]))
close = app.BuildKeyboard(([["Close", "close-tab"]]))
global_command = app.BuildKeyboard(([["• Global Commands •", "global-commands-tab"]]))





# /help command for bot
@app.bot.on_message(filters.command("help"), group=-1)
async def start(_, m: Message):
	if m.from_user:
		if m.from_user.id == app.id:
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
			elif bot.BotPic().endswith(".mp4" or ".gif"):
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

		elif m.from_user.id != app.id:
			info = await app.bot.send_photo(
				m.chat.id,
				"./resources/images/tron.png",
				f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
				reply_markup=InlineKeyboardMarkup(
					[global_command]
				),
			)
		app.message_ids.update({info.chat.id : info.message_id})
	else:
		return




