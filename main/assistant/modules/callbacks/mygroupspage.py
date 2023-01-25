"""
This file creates pages for settings in help menu.
"""

import os
from pyrogram import filters, enums
from pyrogram.types import (
    CallbackQuery,
    InputMediaPhoto
)

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("mygroups-tab"))
@app.alert_user
async def mygroups_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text="<i>Fetching Your Groups . . .</i>",
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            )
        )
        buttons = [
            [app.buildButton(x.chat.title, str(x.chat.id))] async for x in 
            app.get_dialogs() if x.chat.type == enums.ChatType.SUPERGROUP and 
            x.chat.is_creator
        ] + [
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            ]
        await cb.edit_message_text(
            text="Available Groups That Belong To You.",
            reply_markup=app.buildMarkup(*buttons)
        )
    except Exception as e:
        await app.error(e)


@app.bot.on_callback_query(filters.regex(r"-(\d+)"))
async def mygroups_info_callback(_, cb: CallbackQuery):
    try:
        print(cb)
        chat_id = cb.data
        try:
            chat = await app.get_chat(chat_id)
        except PeerInvalid:
            return await cb.answer(
                "Peer Id Invalid.",
                show_alert=True
            )

        if chat.photo:
            path = await app.download_media(chat.photo.big_file_id)
        else:
            path = None

        print(chat.photo, path)
        if path:
            await cb.edit_message_media(
                media=InputMediaPhoto(
                    media=path,
                    caption="Will be added later."
                ),
                reply_markup=app.buildMarkup(
                    [
                        app.buildButton("Home", "close-tab"),
                        app.buildButton("Back", "mygroup-tab")
                    ]
                )
            )
        else:
            await cb.edit_message_media(
            text="Will be added Later.",
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "mygroups-tab")
                ]
            )
        )
    except Exception as e:
        await app.error(e)
