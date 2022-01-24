from pyrogram import filters

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




settings = app.BuildKeyboard((["• Settings •", "open-settings-dex"], ["• Modules •", "tron-dex-2"]))
extra = app.BuildKeyboard((["• Extra •", "open-extra-dex"], ["• Stats •", "open-stats-dex"]))
about = app.BuildKeyboard(([["About", "open-about-dex"]]))
close = app.BuildKeyboard(([["Close", "close-dex"]]))
approve = app.BuildKeyboard(([["Approve", "approve-user"]]))
global_command = app.BuildKeyboard(([["• Global commands •", "global-commands"]]))
home_back = app.BuildKeyboard((["Home", "close-dex"], ["Back", "open-start-dex"]))






# via bot messages
@app.bot.on_inline_query(filters.user(app.id))
def inline_result(_, inline_query):
	query = inline_query.query
	if query.startswith("#p0e3r4m8i8t5"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.PMPERMIT_PIC,
				title="Tron security system",
				description="This is tron security system, it helps you to stop spammers from spamming in your dm.",
				caption=app.PMPERMIT_TEXT,
				parse_mode="combined",
				reply_markup=InlineKeyboardMarkup([approve])
			)
			],
		cache_time=1
		)
	elif query.startswith("#t5r4o9nn6"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.BotPic(),
				title="Introduction to tron",
				description="This is the tron helpdex menu.",
				caption="**Dex:** Home\n\n**Description:** This is your helpdex use this to navigate in different sub dex, guidence and information is given in each dex.",
				parse_mode="combined",
				reply_markup=InlineKeyboardMarkup([settings, extra, about, close])
			)
			],
		cache_time=1
		)
	elif query.startswith("#i2l8v3"):
		inline_query.answer(
		results=[
			InlineQueryResultPhoto(
				photo_url=app.ialive_pic(),
				title="Inline alive",
				description="This is same as alive command, the difference is that this command have inline button.",
				caption=f"**⛊  Inline Status:**\n\n**⟐** {Config.USER_BIO}\n\n**⟜ Owner**: [{USER_NAME}](https://t.me/{USER_USERNAME})\n**⟜ Tron:** `{userbot_version}`\n**⟜ Python:** `{python_version}`\n⟜ **Pyrogram:** `{pyrogram_version}`\n⟜ **uptime:** `{uptime()}\n\n",
				parse_mode="combined",
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
				input_message_content=InputTextMessageContent(app.quote()),
				description="Get infinite anime character quotes through this inline loop button.",
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
