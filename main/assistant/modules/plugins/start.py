import time
import traceback

from main.userbot.client import app
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@app.bot.on_message(filters.command("start"), group=-1)
async def send_response(_, m: Message):
    try:
        await m.reply(
            "👋 **Hey there!**\n\nI'm here to assist you with useful features and powerful tools.\n\nType `/help` to get started or just tap the button below:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "📜 Help",
                            callback_data="public-commands-tab",
                        )
                    ]
                ]
            ),
        )
    except Exception:
        print(traceback.format_exc())


@app.bot.on_message(filters.new_chat_members & filters.group & filters.me, group=1)
async def added_to_group_msg(_, m: Message):
    try:
        if m.new_chat_members[0].is_self:
            await app.bot.send_message(
                m.chat.id,
                "🎉 **Hello everyone!**\n\nThanks for adding me to this awesome group!\n\nUse `/help` to see what I can do.\n\nLet's make this group smarter together 🚀",
            )
    except Exception:
        print(traceback.format_exc())
