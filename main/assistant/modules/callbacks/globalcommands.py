"""
This file creates global commands for public users.
"""

from pyrogram import filters

from pyrogram.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	CallbackQuery,
)

from main.userbot.client import app






@app.bot.on_callback_query(filters.regex("public-commands-tab"))
@app.alert_user
async def _public_commands(_, cb: CallbackQuery):
    await cb.edit_message_text(
        text="**Dex:** Extra\n\n**Location:** /home/extra/public commands\n\n**COMMAND:** /start\n**USAGE:** Check that bot is on or off.\n\n**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n**COMMAND:** /id\n**USAGE:** Get your id and chat id.\n\n**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="extra-tab"
                    )
                ]
            ]
        )
    )





@app.bot.on_callback_query(filters.regex("global-commands-tab"))
async def _global_commands(_, cb):
    await cb.edit_message_text(
        text="**Dex:** Public commands\n\nCOMMAND: /start \n**USAGE:** Check that bot is on or off.\n\n**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n**COMMAND:** /id\n**USAGE:** Get id of group and user.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data="back-to-info"
                    )
                ]
            ]
        )
    )


@app.bot.on_callback_query(filters.regex("back-to-info"))
async def _back_to_info(_, cb):
    await cb.edit_message_text(
        text="You can use these public commands, check below.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="• View commands •",
                        callback_data="global-commands-tab"
                    )
                ]
            ]
        )
    )
