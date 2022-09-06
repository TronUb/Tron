"""
This file is for deleting the inline help menu.
"""

import struct
import base64

from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.errors import PeerIdInvalid

from main.userbot.client import app




@app.bot.on_callback_query(filters.regex("delete-tab"))
@app.alert_user
async def delete_helpdex(_, cb: CallbackQuery):
    """ delete helpdex handler for help plugin """

    try:
        if cb.inline_message_id:
            dc_id, message_id, chat_id, query_id = struct.unpack(
                "<iiiq",
                base64.urlsafe_b64decode(
                    cb.inline_message_id + '=' * (len(cb.inline_message_id) % 4)
                )
            )

            await app.delete_messages(
                chat_id=int(str(-100) + str(chat_id)[1:]),
                message_ids=message_id
            )
        elif not cb.inline_message_id:
            if cb.message:
                await cb.message.delete()
        else:
            await cb.answer(
                "Message Expired !",
                show_alert=True
            )

    except (PeerIdInvalid, KeyError, ValueError):
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_id
        )
        print(chat_id, message_id)
    except Exception as e:
        await app.error(e)
