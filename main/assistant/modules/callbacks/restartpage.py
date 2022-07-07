import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.userbot.client import app






@app.bot.on_callback_query(filters.regex("restart-tab"))
@app.alert_user
async def _restart_tron(_, cb):
	await cb.edit_message_text(
		text="**Dex:** press confirm to restart.\n\n**Location:** /home/settings/restart bot/confirm\n\nPress the Confirm button to restart userbot...",
		reply_markup=InlineKeyboardMarkup(
			[ 
				[
					InlineKeyboardButton(
						"Confirm", callback_data="confirm-restart-tab",
					),
				],
				[
					InlineKeyboardButton(
						"Home", callback_data="close-tab",
					),
					InlineKeyboardButton(
						"Back", callback_data="settings-tab"
					)
				],
			]
		),
	)


@app.bot.on_callback_query(filters.regex("confirm-restart-tab"))
@app.alert_user
async def _restart_core(_, cb):
	await cb.edit_message_text(
		text="**Dex:** restarting . . .\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Restarting bot... please wait...`", 
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="Back", callback_data=f"settings-tab"
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
			"**Dex:** Restarting . . .\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Failed to restart userbot, please do it manually !!`",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							text="Back", 
							callback_data=f"settings-tab"
						),
					],
				]
			),
		)
	else:
		await cb.edit_message_text(
			"**Dex:** Restarting . . .\n\n**Location:** /home/settings/restart bot/confirm\n\n**Process:** `Please wait 2-3 minutes to reboot userbot...`",
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							text="Back", 
							callback_data=f"settings-tab"
						),
					],
				]
			),
		)