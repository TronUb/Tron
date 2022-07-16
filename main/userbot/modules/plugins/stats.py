from main import app, gen
from pyrogram.types import Message




app.CMD_HELP.update(
    {"stats": (
        "stats",
        {
        "stats" : "Get information about how many groups/channels/users you have."
        }
        )
    }
)



@app.on_message(gen("stats", exclude = ["sudo"]))
async def dialogstats_handler(_, m: Message):
    try:
        await app.send_edit("Getting stats . . .", text_type=["mono"])

        bot = 0
        user = 0
        group = 0
        channel = 0
        stat_format = """
        • **STATS FOR:** {}

        🤖 • **BOTS:** {}
        👨 • **USERS:** {}
        🛡️ • **GROUPS:** {}
        ⚙️ • **CHANNELS:** {}
        """

        async for x in app.get_dialogs():
            if x.chat.type == "channel":
                channel += 1
            if x.chat.type == "bot":
                bot += 1
            if x.chat.type in ("supergroup", "group"):
                group += 1
            if x.chat.type == "private":
                user += 1

        await app.send_edit(stat_format.format(app.UserMention(), bot, user, group, channel))
    except Exception as e:
        await app.error(e)
