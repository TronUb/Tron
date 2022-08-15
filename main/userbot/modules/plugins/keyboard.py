""" keyboard plugin """

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from pyrogram.enums import ChatType
from main import app, gen



app.CMD_HELP.update(
    {"heroku" : (
        "heroku",
        {
        "kbd [button text] [url] [caption]" : "get bot custom keyboards",
        }
        )
    }
)



@app.on_message(gen(["kbd", "keyboard"]))
async def create_keyboard(_, m):
    """ create keyboard handler keyboard plugin """
    if not app.GetArgs():
        return await app.send_edit(
            "Give me some args, format: [cmd] [button text] [url] [caption]",
            delme=3,
            text_type=["mono"]
        )

    if m.chat.type in (ChatType.BOT, ChatType.PRIVATE):
        return await app.send_edit("Sorry you can't use it here", delme=3, text_type=["mono"])

    if not await app.user_exists(app.bot.id, m.chat.id):
        return await app.send_edit(
            "Your bot is not present in this group.",
            text_type=["mono"],
            delme=4
        )

    if app.long() >= 3:
        await app.bot.send_message(
            m.chat.id,
            m.text.split(None, 3)[3],
                reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                        m.command[1],
                        url=m.command[2]
                    ),
                    ],
                ]
                )
            )
        await m.delete()
    else:
        await app.send_edit(f"`{app.Trigger()[0]}kbd [ Button text ] [ Button url ] [ Text ]`")
