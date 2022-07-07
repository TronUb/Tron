import heroku3

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery, 
	Message,
)

from main.assistant.client import bot
from main.userbot.client import app





# modules dex
@bot.on_callback_query(filters.regex("modules-tab"))
@app.alert_user
async def modules(_, cb):
	btn = bot.HelpDex(0, bot.CMD_HELP, "navigate")
	await cb.edit_message_text(
		f"**Dex:** Modules \n\n**Location:** /home/modules\n\n**Modules:** `{len(app.CMD_HELP)}`",
		reply_markup=InlineKeyboardMarkup(btn),
	)


# next page
@bot.on_callback_query(filters.regex(pattern="navigate-next\((.+?)\)"))
@app.alert_user
async def give_next_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	buttons = bot.HelpDex(current_page_number + 1, bot.CMD_HELP, "navigate")
	print(cb.matches[0])
	print(dir(cb.matches[0]))
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


# previous page
@bot.on_callback_query(filters.regex(pattern="navigate-prev\((.+?)\)"))
@app.alert_user
async def give_old_page(_, cb):
	current_page_number = int(cb.matches[0].group(1))
	buttons = bot.HelpDex(current_page_number - 1, bot.CMD_HELP, "navigate")
	await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


# back from modules dex to home
@bot.on_callback_query(filters.regex(pattern="back-to-modules-page-(.*)"))
@app.alert_user
async def get_back(_, cb):
	page_number = int(cb.matches[0].group(1))
	buttons = bot.HelpDex(page_number, bot.CMD_HELP, "navigate")
	text = f"**Dex:** Modules\n\nLocation: /home/modules\n\n**Modules:** `{len(bot.CMD_HELP)}`"
	await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))


# modules plugin page information
@bot.on_callback_query(filters.regex(pattern="modulelist-(.*)"))
@app.alert_user
async def give_plugin_cmds(_, cb):
	plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
	plugs = await bot.data(plugin_name)
	help_string = f"MODULE: {plugin_name}\n\n" + "".join(plugs)
	await cb.edit_message_text(
		help_string,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						text="Back",
						callback_data=f"back-to-modules-page-{page_number}",
					)
				]
			]
		),
		)
