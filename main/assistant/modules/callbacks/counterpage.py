"""
This file creates extra page tab menu in helpdex
"""

import struct
from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("counter-tab"))
async def counter_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text=str(0),
            reply_markup=app.buildMarkup(
                [app.buildButton("Increment", "counter-increment-tab")]
            )
        )
    except Exception as e:
        await app.error(e)




@app.bot.on_callback_query(filters.regex("counter-increment-tab"))
async def counter_callback(_, cb: CallbackQuery):
    try:
        if cb.message:
            message = cb.message
        else:
            dc_id, message_id, chat_id, query_id = struct.unpack(
                    "<iiiq",
                    base64.urlsafe_b64decode(
                        cb.inline_message_id + '=' * (
                            len(cb.inline_message_id) % 4
                        )
                    )
                )

            print(chat_id, message_id)
            message = await app.get_messages(chat_id, message_id)
            print(message)

        if message:
            text = getattr(message, "caption", None)

        count = int(text) + 1 if text else 0
        await cb.edit_message_text(
            text=str(count),
            reply_markup=app.buildMarkup(
                [app.buildButton("Increment", "counter-increment-tab")]
            )
        )
    except Exception as e:
        await app.error(e)
