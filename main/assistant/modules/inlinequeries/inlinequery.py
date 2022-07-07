from pyrogram import filters

from pyrogram.enums import ParseMode

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	InlineQueryResultArticle, 
	InlineQueryResultPhoto, 
	InputTextMessageContent, 
	CallbackQuery, 
	Message,
)

from tronx import app





# via bot messages
@bot.on_inline_query(filters.user(app.id))
def inline_result(_, inline_query):
	query = inline_query.query
	if query.startswith("#pmpermit"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.PmpermitPic(),
				title="Tron security system",
				description="This is tron security system, it helps you to stop spammers from spamming in your dm.",
				caption=app.PmpermitText(),
				parse_mode=ParseMode.DEFAULT,
				reply_markup=InlineKeyboardMarkup([app.BuildKeyboard(([["Approve", "approve-tab"]]))])
			)
			],
		cache_time=1
		)
	elif query.startswith("#helpdex"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.BotPic(),
				title="Introduction to tron",
				description="This is the tron helpdex menu.",
				caption="**Dex:** Home\n\n**Description:** This is your helpdex use this to navigate in different sub dex, guidence and information is given in each dex.",
				parse_mode=ParseMode.DEFAULT,
				reply_markup=InlineKeyboardMarkup(
					[
						app.BuildKeyboard((["• Settings •", "settings-tab"], ["• Modules •", "modules-tab"])),
						app.BuildKeyboard((["• Extra •", "extra-tab"], ["• Stats •", "stats-tab"])),
						app.BuildKeyboard(([["About", "about-tab"]])),
						app.BuildKeyboard(([["Close", "close-tab"]]))
					]
				)
			)
			],
		cache_time=1
		)
	elif query.startswith("#ialive"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.ialive_pic(),
				title="Inline alive",
				description="This is same as alive command, the difference is that this command have inline button.",
				caption=f"**⛊  Inline Status:**\n\n**⟐** {app.USER_BIO}\n\n**⟜ Owner**: [{app.name}](https://t.me/{app.username})\n**⟜ Tron:** `{app.userbot_version}`\n**⟜ Python:** `{app.python_version}`\n⟜ **Pyrogram:** `{app.pyrogram_version}`\n⟜ **uptime:** `{app.uptime()}\n\n",
				parse_mode=ParseMode.DEFAULT,
				reply_markup=InlineKeyboardMarkup([app.BuildKeyboard((["Home", "close-tab"], ["Back", "home-tab"]))])
			)
			],
		cache_time=1
		)
	elif query.startswith("#quote"):
		inline_query.answer(
		results=[
			InlineQueryResultArticle(
				title="Inline quotes",
				input_message_content=InputTextMessageContent(app.quote()),
				description="Get infinite anime character quotes through this inline loop button.",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								"More", callback_data="animequote-tab"
							)
						],
					]
				)
			)
		],
	cache_time=1
	)
