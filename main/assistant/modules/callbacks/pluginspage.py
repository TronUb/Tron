"""
This file creates the plugins page in help menu.
"""

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    CallbackQuery
)

from main.userbot.client import app




# plugins page
@app.bot.on_callback_query(filters.regex("plugins-tab"))
@app.alert_user
async def plugins_page_callback(_, cb: CallbackQuery):
    try:
        btn = app.HelpDex(0, app.CMD_HELP, "navigate")
        await cb.edit_message_text(
            text=app.plugin_tab_string,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except Exception as e:
        await app.error(e)


# plugins next page
@app.bot.on_callback_query(filters.regex(pattern=r"navigate-next\((.+?)\)"))
@app.alert_user
async def plugins_next_page_callback(_, cb: CallbackQuery):
    try:
        current_page_number = int(cb.matches[0].group(1))
        btn = app.HelpDex(current_page_number + 1, app.CMD_HELP, "navigate")
        print(cb.matches[0])
        print(dir(cb.matches[0]))
        await cb.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except Exception as e:
        await app.error(e)


# plugins previous page
@app.bot.on_callback_query(filters.regex(pattern=r"navigate-prev\((.+?)\)"))
@app.alert_user
async def plugins_prev_page_callback(_, cb: CallbackQuery):
    try:
        current_page_number = int(cb.matches[0].group(1))
        btn = app.HelpDex(current_page_number - 1, app.CMD_HELP, "navigate")
        await cb.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except Exception as e:
        await app.error(e)


# back from plugins page to home page
@app.bot.on_callback_query(filters.regex(pattern="back-to-plugins-page-(.*)"))
@app.alert_user
async def back_to_home_page_callback(_, cb: CallbackQuery):
    try:
        page_number = int(cb.matches[0].group(1))
        btn = app.HelpDex(page_number, app.CMD_HELP, "navigate")
        await cb.edit_message_text(
            text=app.plugin_tab_string,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except Exception as e:
        await app.error(e)


# plugin commands information
@app.bot.on_callback_query(filters.regex(pattern="pluginlist-(.*)"))
@app.alert_user
async def plugin_info_page_callback(_, cb: CallbackQuery):
    try:
        plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
        plugs = await app.PluginData(plugin_name)
        cmd_string = f"**PLUGIN:** {plugin_name}\n\n" + "".join(plugs)
        await cb.edit_message_text(
            cmd_string,
            reply_markup=app.buildMarkup(
                [app.buildButton("Back", f"back-to-plugins-page-{page_number}")]
            )
        )
    except Exception as e:
        await app.error(e)
