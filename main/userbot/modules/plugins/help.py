""" help plugin """

import os
import struct
import base64

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import (
    BotInlineDisabled,
    PeerIdInvalid
)
from pyrogram.types import (
    Message,
    CallbackQuery,
)

from main import app, gen




app.CMD_HELP.update(
    {"help" : (
        "help",
        {
        "help [ module name ]" : "Get commands info of that plugin.",
        "help" : "Get your inline help dex.",
        "inline" : "Toggle inline mode to On or Off of your bot through @BotFather",
        "uplugs" : "Get list of available userbot plugin names",
        "aplugs" : "Get list of available assistant plugin names",
        }
        )
    }
)



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




@app.on_message(gen("help"))
async def helpmenu_handler(_, m: Message):
    """ helpmenu handler for help plugin """

    args = m.command if app.long() > 1 else None

    try:
        if not args:
            await app.send_edit(". . .", text_type=["mono"])
            result = await app.get_inline_bot_results(
                app.bot.username,
                "#helpmenu"
            )
            if result:
                await m.delete()
                info = await app.send_inline_bot_result(
                    m.chat.id,
                    query_id=result.query_id,
                    result_id=result.results[0].id,
                    disable_notification=True,
                )

            else:
                await app.send_edit(
                    "Please check your bots inline mode is on or not . . .",
                    delme=3,
                    text_type=["mono"]
                )
        elif args:

            module_help = await app.PluginData(args[1])
            if not module_help:
                await app.send_edit(
                    f"Invalid plugin name specified, use `{app.Trigger()[0]}uplugs` to get list of plugins",
                    delme=3
                )
            else:
                await app.send_edit(f"**MODULE:** {args[1]}\n\n" + "".join(module_help))
        else:
            await app.send_edit("Try again later !", text_type=["mono"], delme=3)
    except BotInlineDisabled:
        await app.toggle_inline()
        await helpmenu_handler(_, m)
    except Exception as e:
        await app.error(e)




# get all module name
@app.on_message(gen("uplugs"))
async def uplugs_handler(_, m: Message):
    """ uplugs handler for help plugin """
    store = []
    store.clear()
    for x in os.listdir("main/userbot/modules/plugins/"):
        if not x in ["__pycache__", "__init__.py"]:
            store.append(x + "\n")

    await app.send_edit("**PLUGINS OF USERBOT:**\n\n" + "".join(store))




# get all plugins name
@app.on_message(gen("aplugs"))
async def aplugs_handler(_, m: Message):
    """ aplugs handler for help plugin """
    store = []
    store.clear()
    for x in os.listdir("main/assistant/modules/plugins/"):
        if not x in ["__pycache__", "__init__.py"]:
            store.append(x + "\n")

    await app.send_edit("**PLUGINS OF ASSISTANT:**\n\n" + "".join(store))




@app.on_message(gen("inline"))
async def toggleinline_handler(_, m: Message):
    """ toggleinline handler for help plugin """
    return await app.toggle_inline()
