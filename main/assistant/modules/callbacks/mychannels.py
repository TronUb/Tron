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
channel_info = dict()


async def update_buttons():
    buttons.clear() # remove previous data
    async for x in app.get_dialogs():
        if x.chat.type == enums.ChatType.CHANNEL:
            if x.chat.is_creator:
                buttons.append(
                    [app.buildButton(x.chat.title, str(x.chat.id)+"c")]
                )
    buttons.append(
        [
            app.buildButton("Home", "close-tab"),
            app.buildButton("Refresh", "mychannels-refresh-tab"),
            app.buildButton("Back", "extra-tab")
        ]
    )




@app.bot.on_callback_query(filters.regex(r"(mychannels)(-[a-z]+)?-tab"))
@app.alert_user
async def mychannels_callback(_, cb: CallbackQuery):
    try:
        await cb.edit_message_text(
            text="<i>Fetching Your Channels . . .</i>",
            reply_markup=app.buildMarkup(
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Refresh", "mychannels-refresh-tab"),
                    app.buildButton("Back", "extra-tab")
                ]
            )
        )

        if not buttons or cb.data == "mychannels-refresh-tab": # empty list acts as False
            await update_buttons()

        await cb.edit_message_text(
            text=f"**Total Channels:** `{len(buttons)}`",
            reply_markup=app.buildMarkup(*buttons)
        )
    except Exception as e:
        await app.bot.error(e)


@app.bot.on_callback_query(filters.regex(r"-(\d+)c"))
async def mychannels_info_callback(_, cb: CallbackQuery):
    try:
        chat_id = cb.data.strip("c")
        if channel_info.get(chat_id):
            chat = channel_info.get(chat_id)
        else:
            try:
                chat = await app.get_chat(chat_id)
                channel_info.update({chat_id: chat})
            except PeerInvalid:
                return await cb.answer(
                    "Peer Id Invalid.",
                    show_alert=True
                )

        if not chat:
            await cb.answer(
                "Peer Id Invalid",
                show_alert=True
            )

        if chat.photo:
            path = await app.download_media(chat.photo.big_file_id)
        else:
            path = None

        text = "**Title:** `{}`\n".format(chat.title)
        text += "**Username:** `{}`\n".format(chat.username or '')
        text += "**Id:** `{}`\n".format(chat.id)
        text += "**Type:** `{}`\n".format(chat.type.value)
        text += "**Description:** `{}`\n".format(chat.description or '')
        text += "**Content Protected:** `{}`\n".format('Yes' if chat.has_protected_content else 'No')
        text += "**Member Count:** `{}`\n".format(chat.members_count)

        if path:
            await cb.edit_message_media(
                media=InputMediaPhoto(
                    media=app.BotPic,
                    caption=text
                ),
                reply_markup=app.buildMarkup(
                    [app.buildButton("Open Chat", url=f"https://t.me/c/{str(chat.id)[4:]}/-1")],
                    [
                        app.buildButton("Home", "close-tab"),
                        app.buildButton("Back", "mychannels-tab")
                    ]
                )
            )
            os.remove(path)
        else:
            await cb.edit_message_text(
            text=text,
            reply_markup=app.buildMarkup(
                [app.buildButton("Open Chat", url=f"https://t.me/c/{str(chat.id)[4:] if str(chat.id).startswith('-100') else str(chat.id)[1:]}/-1")],
                [
                    app.buildButton("Home", "close-tab"),
                    app.buildButton("Back", "mychannels-tab")
                ]
            )
        )
    except Exception as e:
        await app.bot.error(e)
