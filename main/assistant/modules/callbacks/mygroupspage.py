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




buttons = []
chat_info = dict()

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

        if not buttons: # empty list acts as False
            async for x in app.get_dialogs():
                if x.chat.type == enums. ChatType.SUPERGROUP:
                    if x.chat.is_creator:
                        buttons.append(
                            [
                                app.buildButton(x.chat.title, str(x.chat.id))
                            ]
                        )
            buttons.append(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            )

        await cb.edit_message_text(
            text=f"**Total Groups:** `{len(buttons)}`",
            reply_markup=app.buildMarkup(*buttons)
        )
    except Exception as e:
        await app.error(e)


@app.bot.on_callback_query(filters.regex(r"-(\d+)"))
async def mygroups_info_callback(_, cb: CallbackQuery):
    try:
        chat_id = cb.data
        if chat_info.get(chat_id):
            chat = chat_info.get(chat_id)
        else:
            try:
                chat = await app.get_chat(chat_id)
                chat_info.update({chat_id: chat})
            except PeerInvalid:
                return await cb.answer(
                    "Peer Id Invalid.",
                    show_alert=True
                )

        if chat and chat.photo:
            path = await app.download_media(chat.photo.big_file_id)
        else:
            path = None

        text = f"**Title:** `{chat.title}`\n"
        text += f"**Username:** `{chat.username or ''}`\n"
        text += f"**Id:** `{chat.id}`\n"
        text += f"**Description:** `{chat.description or '''}`\n"
        text += f"**Content Protected:** `{'Yes' if chat.has_protected_content else 'No'}`\n" 
        text += f"**Member Count:** `{chat.members_count}`\n"

        if path:
            await cb.edit_message_media(
                media=InputMediaPhoto(
                    media=path,
                    caption=text
                ),
                reply_markup=app.buildMarkup(
                    [
                        app.buildButton("Home", "close-tab"),
                        app.buildButton("Back", "mygroups-tab")
                    ]
                    )
            )
        else:
            await cb.edit_message_media(
            text=text,
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "mygroups-tab")
                ]
            )
        )
    except Exception as e:
        await app.error(e)
