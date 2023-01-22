"""
This file creates extra page tab menu in helpdex
"""
import struct
import base64

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app



reply_markup=app.buildMarkup(
    [
        app.buildButton("1", "cal-(1)"),
        app.buildButton("2", "cal-(2)"),
        app.buildButton("3", "cal-(3)"),
        app.buildButton("-", "cal-(-)")
    ],
    [
        app.buildButton("4", "cal-(4)"),
        app.buildButton("5", "cal-(5)"),
        app.buildButton("6", "cal-(6)"),
        app.buildButton("+", "cal-(+)")
    ],
    [
        app.buildButton("7", "cal-(7)"),
        app.buildButton("8", "cal-(8)"),
        app.buildButton("9", "cal-(9)"),
        app.buildButton("×", "cal-(*)")
    ],
    [
        app.buildButton("0", "cal-(0)"),
        app.buildButton("C", "cal-(C)"),
        app.buildButton("del", "cal-(D)"),
        app.buildButton("÷", "cal-(/)")
    ],
    [app.buildButton("=", "cal-(=)")]
    [
        app.buildButton("Home", "close-tab"),
        app.buildButton("Back", "extra-tab")
    ]
)


@app.bot.on_callback_query(filters.regex("calculator-tab"))
async def calculator_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text=" ",
            reply_markup=reply_markup
        )
    except Exception as e:
        await app.error(e)




@app.bot.on_callback_query(filters.regex(r"."))
async def calculator_evaluate_callback(_, cb: CallbackQuery):
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
            return

        ch = cb.data[-2]
        caption = message.caption if message.caption else ""

        if ch=="C":
            text = ""
        elif ch=="D":
            text = caption[:-1]
        elif ch=="=":
            try:
                text = eval(caption) if caption else ""
            except Exception as e:
                text = "Error !"
        else:
            text = caption + ch

        await cb.edit_message_text(
            text=text,
            reply_markup=reply_markup
        )
    except Exception as e:
        await app.error(e)
