"""
This file creates extra page tab menu in helpdex
"""

import struct
import base64

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app


@app.bot.on_callback_query(filters.regex("counter-tab"))
async def counter_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text=str(0),
            reply_markup=app.buildMarkup(
                [app.buildButton("Increment", "counter-increment-tab")],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            )
        )
    except Exception as e:
        await app.error(e)


@app.bot.on_callback_query(filters.regex("counter-increment-tab"))
async def counter_increment_callback(_, cb: CallbackQuery):
    try:
        if cb.inline_message_id:
            dc_id, message_id, chat_id, query_id = struct.unpack(
                "<iiiq",
                base64.urlsafe_b64decode(
                    cb.inline_message_id + '=' * (
                        len(cb.inline_message_id) % 4
                    )
                )
            )

            message = await app.get_messages(
                chat_id=int(str(-100) + str(chat_id)[1:]),
                message_ids=message_id
            )
        elif cb.message:
            message = cb.message
        else:
            message = None

        if message:
            text = getattr(message, "caption", None)

        count = int(text) + 1 if text else 0
        await cb.edit_message_text(
            text=str(count),
            reply_markup=app.buildMarkup(
                [app.buildButton("Increment", "counter-increment-tab")],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            )
        )
    except Exception as e:
        await app.error(e)
