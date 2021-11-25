import os
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




# buttons
settings = build_keyboard((["• Settings •", "open-settings-dex"], ["• Modules •", "tron-dex-2"]))
extra = build_keyboard((["• Extra •", "open-extra-dex"], ["• Stats •", "open-stats-dex"]))
about = build_keyboard(([["About", "open-about-dex"]]))
close = build_keyboard(([["Close", "close-dex"]]))
approve = build_keyboard(([["Approve", "approve-user"]]))
global_command = build_keyboard(([["• Global commands •", "global-commands"]]))
home_back = build_keyboard((["Home", "close-dex"], ["Back", "open-start-dex"]))




# modules dex
@bot.on_callback_query(filters.regex("tron-dex-2") & filters.user(USER_ID))
async def modules(_, cb):
	official = True
	cmd = CMD_HELP
	btn = helpdex(0, CMD_HELP, "helpme", official=official)
	await cb.edit_message_text(
		f"**Dex:** Modules \n\n**Location:** /home/modules\n\n**Modules:** `{len(cmd)}`",
		reply_markup=InlineKeyboardMarkup(btn),
	)




# next page
@bot.on_callback_query(filters.regex(pattern="helpme_next\((.+?)\)_(True|False)") & filters.user(USER_ID))
async def give_next_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	official = True
	if cb.matches[0].group(2) == "False":
		official = False
	cmd_help = CMD_HELP if official else cmd_help
	buttons = helpdex(
		current_page_number + 1, cmd_help, "helpme", official=official
	)
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))




# previous page
@bot.on_callback_query(filters.regex(pattern="helpme_prev\((.+?)\)_(True|False)") & filters.user(USER_ID))
async def give_old_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	official = True
	if cb.matches[0].group(2) == "False":
		official = False
	cmd_help = CMD_HELP if official else CMD_HELP
	buttons = helpdex(
		current_page_number - 1, cmd_help, "helpme", official=official
	)
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))




# back from modules dex to home
@bot.on_callback_query(filters.regex(pattern="backme_(.*)_(True|False)") & filters.user(USER_ID))
async def get_back(_, cb):
	page_number = int(cb.matches[0].group(1))
	official = True
	if cb.matches[0].group(2) == "False":
		official = False
	cmd_help = CMD_HELP if official else CMD_HELP
	buttons = helpdex(page_number, cmd_help, "helpme", official=official)
	text = f"**Dex:** Modules\n\nLocation: /home/modules\n\n**Modules:** `{len(cmd_help)}`"
	await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))




# modules plugin page information
@bot.on_callback_query(filters.regex(pattern="modulelist_(.*)_(True|False)") & filters.user(USER_ID))
async def give_plugin_cmds(_, cb):
	plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
	official = True
	if cb.matches[0].group(2) == "False":
		official = False
	plugs = await data(plugin_name)
	help_string = f"PLUGIN: {plugin_name}\n\n" + "".join(plugs)
	await cb.edit_message_text(
		help_string,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="Back",
						callback_data=f"backme_{page_number}_{official}",
					)
				]
			]
		),
		)





# list of helpdex
@bot.on_callback_query(filters.regex("open-stats-dex"))
async def _stats(_, cb):
	await alert_user(cb)
	await cb.edit_message_text(
		text=f"**Dex:** Stats\n\n**Location:** /home/stats\n\nName: {USER_NAME}\nLara version: {lara_version}\nPython version: {__python_version__}\nPyrogram: {__pyro_version__}\nDB_URI: {db_status}\nUptime: {uptime()}\n\nUser Bio: {Config.USER_BIO}",
		reply_markup=InlineKeyboardMarkup([home_back]),
	)


# about info
@bot.on_callback_query(filters.regex("open-about-dex") & filters.user(USER_ID))
async def _about(_, cb):
	if filters.regex("open-about-dex"):
		await cb.edit_message_text(
			text="**Dex:** About\n\n**Location:** /home/about\n\n[ Personal Info ]:\n\nAge: 19\nName: Lara\nGender: Female\n\n[ Versions ]:\n\nPython : v.3.9.4\nPyrogram: v.1.2.8\nAssistant:  v.0.0.1\n\n[ About ]:\n\nI am Lara made by ࿇•ẞᗴᗩSԵ•࿇\nFrom now on i am your friendly assistant. You can ask me for any help related to your userbot.",
			reply_markup=InlineKeyboardMarkup([home_back]),
		)


@bot.on_callback_query(filters.regex("public-commands") & filters.user(USER_ID))
async def _public(_, cb):
	if filters.regex("public-commands"):
		await cb.edit_message_text(
			text="**Dex:** Extra\n\n**Location:** /home/extra/public commands\n\n**COMMAND:** /start\n**USAGE:** Check that bot is on or off.\n\n**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n**COMMAND:** /id\n**USAGE:** Get your id and chat id.\n\n**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"Back", callback_data="open-extra-dex",
						),
					]
				]
			),
		)

@bot.on_callback_query(filters.regex("open-extra-dex") & filters.user(USER_ID))
async def _extra(_, cb):
	if filters.regex("open-extra-dex"):
		await cb.edit_message_text(
			text="**Dex:** Extra\n\nLocation: /home/extra",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"• Public commands •",
							callback_data="public-commands"
							)
					],
					[
						InlineKeyboardButton(
							"Home",
							callback_data="close-dex"
							),
						InlineKeyboardButton(
							"Back",
							callback_data="open-start-dex"
							)
					],
				]
			),
		)


@bot.on_callback_query(filters.regex("close-dex") & filters.user(USER_ID))
async def _close(_, cb: CallbackQuery):
	if filters.regex("close-dex"):
		await cb.edit_message_text(
			text="Welcome to Tron.\n\nThis is your Helpdex, Tap on open button to get more buttons which will help you to understand & operate your userbot & assistant ( LARA ).\n\n• Menu is closed.",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"Open", callback_data="open-start-dex",
						)
					],
					[
						InlineKeyboardButton(
							"Delete", callback_data="delete-dex",
						)
					]
				]
			),
		)



@bot.on_callback_query(filters.regex("open-settings-dex") & filters.user(USER_ID))
async def _settings(_, cb):
	if filters.regex("open-settings-dex"):
		await cb.edit_message_text(
			text="**Dex:** Settings\n\n**Location:** /home/settings",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"Restart bot", callback_data="restart-tron",
						),
					],
					[
						InlineKeyboardButton(
							"Shutdown bot", callback_data="shutdown-tron",
						)
					],
					home_back,
				]
			),
		)


@bot.on_callback_query(filters.regex("open-start-dex") & filters.user(USER_ID))
async def _start(_, cb):
	if filters.regex("open-start-dex"):
		await cb.edit_message_text(
			text = "**Dex:** Home\n\n**Description:** This is your helpdex use to navigate in different sub dex to information.",
			reply_markup=InlineKeyboardMarkup(
				[settings, extra, about, close]
			),
		)

@bot.on_callback_query(filters.regex("restart-tron") & filters.user(USER_ID))
async def _restart_tron(_, cb):
	if filters.regex("restart-tron"):
		await cb.edit_message_text(
			text="**Dex:** restart bot ( before confirm )\n\n**Location:** /home/settings/restart bot/confirm\n\nPress the Confirm button to restart userbot...",
			reply_markup=InlineKeyboardMarkup(
				[ 
					[
						InlineKeyboardButton(
							"Confirm", callback_data="restart-core",
						),
					],
					[
						InlineKeyboardButton(
							"Home", callback_data="close-dex",
						),
						InlineKeyboardButton(
							"Back", callback_data="open-settings-dex"
						)
					],
				]
			),
		)

@bot.on_callback_query(filters.regex("restart-core") & filters.user(USER_ID))
async def _restart_core(_, cb):
	if filters.regex("restart-core"):
		await cb.edit_message_text(
			text="**Dex:** restart bot ( after confirm )\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Restarting bot... please wait...`", 
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							text="Back", callback_data=f"open-settings-dex"
						),
					],
				]
			),
		)
		access = heroku3.from_key(Config.HEROKU_API_KEY)
		application = access.apps()[Config.HEROKU_APP_NAME]
		restart = application.restart()
		if not restart:
			await cb.edit_message_text(
				"**Dex:** restart bot ( after confirm )\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Failed to restart userbot, please do it manually !!`",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								text="Back", 
								callback_data=f"open-settings-dex"
							),
						],
					]
				),
			)
		else:
			await cb.edit_message_text(
				"**Dex:** restart bot ( before confirm )\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Please wait 2-3 minutes to reboot userbot...`",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								text="Back", 
								callback_data=f"open-settings-dex"
							),
						],
					]
				),
			)

@bot.on_callback_query(filters.regex("shutdown-tron") & filters.user(USER_ID))
async def _shutdown_tron(_, cb):
	if filters.regex("shutdown-tron"):
		await cb.edit_message_text(
			text="**Dex:** shutdown bot ( before confirm )\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** Press the Confirm button to shutdown the userbot...",
			reply_markup=InlineKeyboardMarkup(
				[ 
					[
						InlineKeyboardButton(
							"Confirm", 
							callback_data="shutdown-core",
						),
					],
					[
						InlineKeyboardButton(
							"Home", callback_data="close-dex",
						),
						InlineKeyboardButton(
							"Back", callback_data="open-settings-dex"
						)
					],
				]
			),
		)

@bot.on_callback_query(filters.regex("shutdown-core"))
async def _shutdown_core(_, cb):
	await alert_user(cb)
	if filters.regex("shutdown-core"):
		await cb.edit_message_text(
			text="**Dex:** shutdown bot ( after confirm )\n\n**Location:** /home/settings/shutdown bot/confirm\n\n`Turning the userbot off, please wait...`", 
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							text="Back", 
							callback_data=f"open-settings-dex"
						),
					],
				]
			),
		)
		access = heroku3.from_key(Config.HEROKU_API_KEY)
		application = access.apps()[Config.HEROKU_APP_NAME]
		if not application:
			await cb.edit_message_text(
				"**Dex:** shutdown bot ( after confirm )\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** `Failed to turn userbot off, please do it manually !!`",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton(
								text="Back", 
								callback_data=f"open-settings-dex"
							),
						],
					]
				),
			)
		else:
			if application:
				application.process_formation()["worker"].scale(0)
				await cb.edit_message_text(
					"**Dex:** shutdown bot ( after confirm )\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** `Turned off the userbot... If Needed then please turn on the bot manually..`",
					reply_markup=InlineKeyboardMarkup(
						[
							[
								InlineKeyboardButton(
									text="Back", 
									callback_data=f"open-settings-dex"
								),
							],
						]
					),
				)
			else:
				sys.exit(0)

@bot.on_callback_query(filters.regex("more-anime-quotes"))
async def _more_anime_quotes(_, cb):
	await alert_user(cb)
	await cb.edit_message_text(
		quote(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"More", 
						callback_data="more-anime-quotes",
					),
				]
			]
		),
	)


@bot.on_callback_query(filters.regex("global-commands"))
async def _global_commands(_, cb):
	if filters.regex("global-commands"):
		await cb.edit_message_text(
			text="**Dex:** Public commands\n\nCOMMAND: /start \n**USAGE:** Check that bot is on or off.\n\n**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n**COMMAND:** /anime\n**USAGE:** Search anime to get anime information.\n\n**COMMAND:** /manga\n**USAGE:** Search manga to get manga information.\n\n**COMMAND:** /airing\n**USAGE:** Search ongoing anime and get information.\n\n**COMMAND:** /character\n**USAGE:** Search anime character and get their information.\n\n**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"Back", callback_data="back-to-info",
						),
					]
				]
			),
		)


@bot.on_callback_query(filters.regex("back-to-info"))
async def _back_to_info(_, cb):
	if filters.regex("back-to-info"):
		await cb.edit_message_text(
			f"You are a global user that's why you can use these commands, check below.",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"• View commands •", callback_data="global-commands",
						)
					]
				]
			),
		)




async def alert_user(cb):
	if not cb.from_user.id == USER_ID:
		await cb.answer(
			"Sorry you can't use this userbot , make your own userbot at @tronuserbot !",
			show_alert=True,
		)
	return

# ---------------- The End ---------------------------------------
