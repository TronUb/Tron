"""
broadcast messages to all users who started assistant bot.
"""

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

from main.userbot.client import app




@app.bot.on_message(filters.command("broadcast") & filters.private & filters.user(app.id))
async def bot_broadcast_handler(_, m: Message):
    tlen = len(m.text.split())

    if tlen == 1:
        return await app.bot.send_message(
            m.from_user.id,
            "Give me some broadcasting message."
        )

    text = m.text.split(None, 1)[1]
    count = 0

    for user_id in app.getdv("BOT_STARTED_ID"):
        try:
            await app.bot.resolve_peer(user_id)
            done = await app.bot.send_message(user_id, text)
            if done:
                count += 1
        except PeerIdInvalid:
            pass
    await app.bot.send_message(
        m.from_user.id,
        f"Broadcast done, messages sent to {count} users."
    )




@app.bot.on_message(filters.private & filters.text & ~filters.user(app.id), group=1)
async def bot_botstarted_handler(_, m: Message):
    user = m.from_user
    if user and m.text == "/start":
        idlist = app.getdv("BOT_STARTED_ID")
        if idlist:
            if m.from_user.id in idlist:
                return

            newvalue = str(idlist.append(user.id))
        else:
            newvalue = str([m.from_user.id])

        app.setdv("BOT_STARTED_ID", newvalue)
