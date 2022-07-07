import sys
import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot






@bot.on_callback_query(filters.regex("shutdown-tab"))
@app.alert_user
async def _shutdown_tron(_, cb):
	await cb.edit_message_text(
		text="**Dex:** press confirm to shutdown.\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** Press the Confirm button to shutdown the userbot...",
		reply_markup=InlineKeyboardMarkup(
			[ 
				[
					InlineKeyboardButton(
						"Confirm", 
						callback_data="confirm-shutdown",
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


@bot.on_callback_query(filters.regex("confirm-shutdown"))
@app.alert_user
async def _shutdown_core(_, cb):
	await cb.edit_message_text(
		text="**Dex:** shutdown in process.\n\n**Location:** /home/settings/shutdown bot/confirm\n\n`Turning the userbot off, please wait...`", 
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
	access = heroku3.from_key(app.HEROKU_API_KEY)
	application = access.apps()[app.HEROKU_APP_NAME]
	if not application:
		await cb.edit_message_text(
			"**Dex:** shutdown in process.\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** `Failed to turn userbot off, please do it manually !!`",
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
		if application:
			application.process_formation()["worker"].scale(0)
			await cb.edit_message_text(
				"**Dex:** shutdown in process.\n\n**Location:** /home/settings/shutdown bot/confirm\n\n**Process:** `Turned off the userbot... If Needed then please turn on the bot manually..`",
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
			sys.exit(0)