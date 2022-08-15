""" ping pplugin """

import random
import asyncio

from datetime import datetime

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"ping" : (
        "ping",
        {
        "ping" : "Shows you the response speed of the bot.",
        "ping [ number ]" : "Make infinite pings, don't overuse."
        }
        )
    }
)




# animations
data = [
    "🕜",
    "🕡",
    "🕦",
    "🕣",
    "🕥",
    "🕧",
    "🕓",
    "🕔",
    "🕒",
    "🕑",
    "🕐"
]

pings = []




@app.on_message(gen(["ping", "pong"]))
async def ping_handler(_, m: Message):
    """ ping handler for ping plugin """
    try:

        if app.long() == 1:
            start = datetime.now()
            await app.send_edit(". . .", text_type=["mono"])
            end = datetime.now()
            m_s = (end - start).microseconds / 1000
            await app.send_edit(
                f"**Pöng !**\n`{m_s} ms`\n⧑ {app.UserMention()}",
                disable_web_page_preview=True
            )
        elif app.long() == 2:
            cmd = m.command
            count = int(cmd[1]) if cmd[1] and cmd[1].isdigit() else 0
            if count <= 1:
                return await app.send_edit(
                    f"Use `{app.Trigger()[0]}ping` for pings less than 1.",
                    delme=3
                )

            else:
                try:
                    for _ in range(count):
                        await infinite()
                        await app.send_edit(". . .", text_type=["mono"])
                        await asyncio.sleep(0.30)
                    await app.send_edit("".join(pings))
                    pings.clear()
                except Exception as e:
                    await app.error(e)
        else:
            return await app.send_edit("Something went wrong in ping module.", delme=2)
    except Exception as e:
        await app.error(e)




# function to create lots of pings
async def infinite():
    """ infinite function for ping plugin """
    start = datetime.now()
    await app.send_edit(random.choice(data)) # MessageNotModified
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    msg = f"Pöng !\n{m_s} ms\n⧑ {app.UserMention()}\n\n"
    pings.append(msg)
    return True
