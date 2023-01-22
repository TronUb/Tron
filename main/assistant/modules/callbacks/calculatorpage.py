"""
This file creates extra page tab menu in helpdex
"""

from pyrogram import filters
from pyrogram.types import CallbackQuery

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("calculator-tab"))
async def calculator_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text=" ",
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("1", "one-tab"),
                    app.buildButton("2", "two-tab"),
                    app.buildButton("3", "three-tab"),
                    app.buildButton("-", "subtraction-tab")
                ],
                [
                    app.buildButton("4", "four-tab"),
                    app.buildButton("5", "five-tab"),
                    app.buildButton("6", "six-tab"),
                    app.buildButton("+", "addition-tab")
                ],
                [
                    app.buildButton("7", "seven-tab"),
                    app.buildButton("8", "eight-tab"),
                    app.buildButton("9", "nine-tab"),
                    app.buildButton("×", "multiplication-tab")
                ],
                [
                    app.buildButton("0", "zero-tab"),
                    app.buildButton("C", "clear-tab"),
                    app.buildButton("del", "del-tab"),
                    app.buildButton("=", "equate-tab")
                ]
                
            )
        )
    except Exception as e:
        await app.error(e)
