"""
to-do
"""

from pyrogram import filters
from pyrogram.types import Message
from main.userbot.client import app
from pyrogram.errors import PeerIdInvalid





@app.bot.on_message(filters.command("broadcast") & filters.private & filters.user(app.id))
async def broadcast_message(_, m: Message):
    tlen = len(m.text.split())

    if tlen == 1:
        await app.bot.send_message(m.from_user.id, "Give me some broadcasting message.")
        return

    text = m.text.split(None, 1)[1]
    count = 0

    for ids in [int(x) for x in app.getdv("BOT_STARTED_ID").split()]:
        try:
            await app.bot.resolve_peer(ids)
            done = await app.bot.send_message(ids, text)
            if done:
                count += 1
        except PeerIdInvalid:
            pass
    await app.bot.send_message(m.from_user.id, f"Broadcast done, messages sent to {count} users.")




@app.bot.on_message(filters.private & filters.text, group=1)
async def botstartedusers(_, m: Message):
    if m.from_user and m.text == "/start":
        varexists = app.getdv("BOT_STARTED_ID")
        if varexists:
            if m.from_user.id in [int(x) for x in varexists.split()]:
                return

            newvalue = varexists + " " + str(m.from_user.id)
        else:
            newvalue = str(m.from_user.id)

        app.setdv("BOT_STARTED_ID", newvalue)
