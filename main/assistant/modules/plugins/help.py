from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardMarkup, 
	Message,
)

from main.assistant.client import bot





settings = bot.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"]))
extra = bot.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"]))
about = bot.BuildKeyboard(([["About", "about-tab"]]))
close = bot.BuildKeyboard(([["Close", "close-tab"]]))
global_command = bot.BuildKeyboard(([["• Global Commands •", "global-commands-tab"]]))





# /start command for bot
@bot.on_message(filters.command("help"), group=-1)
async def start(_, m: Message):
	if m.from_user:
		if m.from_user.id == bot.id:
			# bot pic
			if bot.BotPic().endswith(".jpg" or "png" or "jpeg"):
				info = await bot.send_photo(
					m.chat.id,
					bot.BotPic(),
					bot.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			elif bot.BotPic().endswith(".mp4" or ".gif"):
				info = await bot.send_photo(
					m.chat.id,
					bot.BotPic(),
					bot.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
						[ settings, extra, about, close ]
					),
				)
			else:
				info = await bot.send_message(
					m.chat.id,
					bot.BotBio(m),
					reply_markup=InlineKeyboardMarkup(
					[ settings, extra, about, close ]
					),
				)

		elif m.from_user.id != bot.id:
			info = await bot.send_photo(
				m.chat.id,
				"./resources/images/tron.png",
				f"Hey {m.from_user.mention} You are eligible to use me. There are some commands you can use, check below.",
				reply_markup=InlineKeyboardMarkup(
					[global_command]
				),
			)
		bot.message_ids.update({info.chat.id : info.message_id})
	else:
		return




