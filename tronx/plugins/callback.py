import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from tronx import app





# buttons
settings = app.BuildKeyboard((["• Settings •", "open-settings-dex"], ["• Modules •", "tron-dex-2"]))
extra = app.BuildKeyboard((["• Extra •", "open-extra-dex"], ["• Stats •", "open-stats-dex"]))
about = app.BuildKeyboard(([["About", "open-about-dex"]]))
close = app.BuildKeyboard(([["Close", "close-dex"]]))
approve = app.BuildKeyboard(([["Approve", "approve-user"]]))
global_command = app.BuildKeyboard(([["• Global commands •", "global-commands"]]))
home_back = app.BuildKeyboard((["Home", "close-dex"], ["Back", "open-start-dex"]))




# modules dex
@app.bot.on_callback_query(filters.regex("tron-dex-2"))
@app.alert_user
async def modules(_, cb):
	btn = app.HelpDex(0, app.CMD_HELP, "helpme")
	await cb.edit_message_text(
		f"**Dex:** Modules \n\n**Location:** /home/modules\n\n**Modules:** `{len(app.CMD_HELP)}`",
		reply_markup=InlineKeyboardMarkup(btn),
	)


# next page
@app.bot.on_callback_query(filters.regex(pattern="helpme_next\((.+?)\)"))
@app.alert_user
async def give_next_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	buttons = app.HelpDex(current_page_number + 1, app.CMD_HELP, "helpme")
	print(cb.matches[0])
	print(dir(cb.matches[0]))
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


# previous page
@app.bot.on_callback_query(filters.regex(pattern="helpme_prev\((.+?)\)"))
@app.alert_user
async def give_old_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	buttons = app.HelpDex(current_page_number - 1, app.CMD_HELP, "helpme")
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


# back from modules dex to home
@app.bot.on_callback_query(filters.regex(pattern="backme_(.*)"))
@app.alert_user
async def get_back(_, cb):
	page_number = int(cb.matches[0].group(1))
	buttons = app.HelpDex(page_number, app.CMD_HELP, "helpme")
	text = f"**Dex:** Modules\n\nLocation: /home/modules\n\n**Modules:** `{len(app.CMD_HELP)}`"
	await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# modules plugin page information
@app.bot.on_callback_query(filters.regex(pattern="modulelist_(.*)"))
@app.alert_user
async def give_plugin_cmds(_, cb):
	plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
	plugs = await app.data(plugin_name)
	help_string = f"PLUGIN: {plugin_name}\n\n" + "".join(plugs)
	await cb.edit_message_text(
		help_string,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="Back",
						callback_data=f"backme_{page_number}",
					)
				]
			]
		),
		)


# list of helpdex
@app.bot.on_callback_query(filters.regex("open-stats-dex"))
@app.alert_user
async def _stats(_, cb):
	await cb.edit_message_text(
		text=app.stat_string(),
		reply_markup=InlineKeyboardMarkup([home_back]),
	)


# about info
@app.bot.on_callback_query(filters.regex("open-about-dex"))
@app.alert_user
async def _about(_, cb):
	await cb.edit_message_text(
		text=f"**Dex:** About\n\n**Location:** /home/about\n\n**[ Personal Info ]:**\n\n**Age:** {app.assistant_age}\n**Name:** {app.assistant_name}\n**Gender:** {app.assistant_gender}\n\n**[ Versions ]:**\n\n**Python:** {app.python_version}\n**Pyrogram:** {app.pyrogram_version}\n**Assistant:**  {app.assistant_version}\n\n**[ About ]:**\n\nI am Nora made by ࿇•ẞᗴᗩSԵ•࿇\nI am your friendly assistant, i will help you as much as you need. You can ask me for any help related to your userbot. If you have any suggestions or you're facing any problems which are related to tronuserbot then just ask in [support group](https://t.me/tronuserbot_support), ",
		reply_markup=InlineKeyboardMarkup([home_back]),
	)


@app.bot.on_callback_query(filters.regex("public-commands"))
@app.alert_user
async def _public(_, cb):
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


@app.bot.on_callback_query(filters.regex("open-extra-dex"))
@app.alert_user
async def _extra(_, cb):
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


@app.bot.on_callback_query(filters.regex("close-dex"))
@app.alert_user
async def _close(_, cb: CallbackQuery):
	await cb.edit_message_text(
		text=app.closed_menu_string(),
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


@app.bot.on_callback_query(filters.regex("open-settings-dex"))
@app.alert_user
async def _settings(_, cb):
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
				[
					InlineKeyboardButton(
						"Update bot", callback_data="update-tron",
					)
				],
				home_back,
			]
		),
	)


@app.bot.on_callback_query(filters.regex("update-tron"))
@app.alert_user
async def _update_callback(_, cb):
	pass


@app.bot.on_callback_query(filters.regex("open-start-dex"))
@app.alert_user
async def _start(_, cb):
	await cb.edit_message_text(
		text = "**Dex:** Home\n\n**Description:** This is your helpdex use to navigate in different sub dex to information.",
		reply_markup=InlineKeyboardMarkup(
			[settings, extra, about, close]
		),
	)


@app.bot.on_callback_query(filters.regex("restart-tron"))
@app.alert_user
async def _restart_tron(_, cb):
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


@app.bot.on_callback_query(filters.regex("restart-core"))
@app.alert_user
async def _restart_core(_, cb):
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
	access = heroku3.from_key(app.HEROKU_API_KEY)
	application = access.apps()[app.HEROKU_APP_NAME]
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


@app.bot.on_callback_query(filters.regex("shutdown-tron"))
@app.alert_user
async def _shutdown_tron(_, cb):
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


@app.bot.on_callback_query(filters.regex("shutdown-core"))
@app.alert_user
async def _shutdown_core(_, cb):
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
	access = heroku3.from_key(app.HEROKU_API_KEY)
	application = access.apps()[app.HEROKU_APP_NAME]
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


@app.bot.on_callback_query(filters.regex("more-anime-quotes"))
async def _more_anime_quotes(_, cb):
	await cb.edit_message_text(
		app.quote(),
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


@app.bot.on_callback_query(filters.regex("global-commands"))
async def _global_commands(_, cb):
	await cb.edit_message_text(
		text="**Dex:** Public commands\n\nCOMMAND: /start \n**USAGE:** Check that bot is on or off.\n\n**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n**COMMAND:** /id\n**USAGE:** Get id of group and user.",
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


@app.bot.on_callback_query(filters.regex("back-to-info"))
async def _back_to_info(_, cb):
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




