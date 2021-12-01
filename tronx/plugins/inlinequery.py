from pyrogram import (
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
	bot = False

from tronx import (
	version, 
	USER_ID, 
	USER_NAME, 
	USER_USERNAME, 
	Config,
	uptime,
	__python_version__,
)

from tronx.helpers import (
	build_keyboard,
	quote,
	ialive_pic,
	bot_pic,
)




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
				photo_url=bot_pic(),
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
