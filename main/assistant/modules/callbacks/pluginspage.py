"""
This file creates the plugins page in help menu.
"""

from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from main.userbot.client import app





# plugins dex
@app.bot.on_callback_query(filters.regex("plugins-tab"))
@app.alert_user
async def plugins_page(_, cb: CallbackQuery):
    btn = app.HelpDex(0, app.CMD_HELP, "navigate")
    await cb.edit_message_text(
        text=app.plugin_tab_string(),
        reply_markup=InlineKeyboardMarkup(btn)
    )


# next page
@app.bot.on_callback_query(filters.regex(pattern="navigate-next\((.+?)\)"))
@app.alert_user
async def give_next_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(current_page_number + 1, app.CMD_HELP, "navigate")
    print(cb.matches[0])
    print(dir(cb.matches[0]))
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# previous page
@app.bot.on_callback_query(filters.regex(pattern="navigate-prev\((.+?)\)"))
@app.alert_user
async def give_old_page(_, cb: CallbackQuery):
    current_page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(current_page_number - 1, app.CMD_HELP, "navigate")
    await cb.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))


# back from plugin dex to home
@app.bot.on_callback_query(filters.regex(pattern="back-to-plugins-page-(.*)"))
@app.alert_user
async def get_back(_, cb: CallbackQuery):
    page_number = int(cb.matches[0].group(1))
    btn = app.HelpDex(page_number, app.CMD_HELP, "navigate")
    await cb.edit_message_text(text=app.plugin_tab_string(), reply_markup=InlineKeyboardMarkup(btn))


# plugin page information
@app.bot.on_callback_query(filters.regex(pattern="pluginlist-(.*)"))
@app.alert_user
async def give_plugin_cmds(_, cb: CallbackQuery):
    plugin_name, page_number = cb.matches[0].group(1).split("|", 1)
    plugs = await app.PluginData(plugin_name)
    cmd_string = f"**PLUGIN:** {plugin_name}\n\n" + "".join(plugs)
    await cb.edit_message_text(
        cmd_string,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Back",
                        callback_data=f"back-to-plugins-page-{page_number}",
                    )
                ]
            ]
        ),
        )
