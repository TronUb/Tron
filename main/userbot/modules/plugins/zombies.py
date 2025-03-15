import os
import asyncio

from pyrogram.types import Message

from main import app, gen
from main.core.enums import UserType


@app.on_cmd(
    commands="zombies",
    usage="Check deleted accounts in chat, use clean as suffix to remove them.",
    disable_for=UserType.SUDO
)
async def zombies_handler(_, m: Message):
    if await app.check_private():
        return

    temp_count = 0
    admin_count = 0
    count = 0

    if app.command() != 2:
        await app.send_edit("Checking deleted accounts . . .", text_type=["mono"])

        async for x in app.get_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                temp_count += 1

        if temp_count > 0:
            await app.send_edit(f"**Found:** `{temp_count}` Deleted accounts\nUse `{app.Trigger[0]}zombies clean` to remove them from group.")
        else:
            await app.send_edit("No deleted accounts found.\nGroup is clean as Hell ! 😃", delme=3, text_type=["mono"])

    elif app.command() == 2 and m.command[1] == "clean":
        await app.send_edit("Cleaning deleted accounts . . .", text_type=["mono"])

        async for x in app.get_chat_members(chat_id=m.chat.id):
            if x.user.is_deleted:
                if x.status in ("administrator", "creator"):
                    admin_count += 1
                    continue
                try:
                    await app.ban_chat_member(
                        chat_id=m.chat.id,
                        user_id=x.user.id
                    )
                    count += 1
                    await asyncio.sleep(0.2)
                except Exception as e:
                    await app.error(e)
        await app.send_edit(f"`Group clean up done !`\n\n**Total:** `{count+admin_count}`\n**Removed:** `{count}`\n**Not Removed:** `{admin_count}`\n\n**Note:** `Not removed accounts can be admins or the owner`")

    elif app.command() == 2 and m.command[1] != "clean":
        await app.send_edit(f"Check `{app.Trigger[0]}help zombies` to see how it works !")
    else:
        await app.send_edit("Something went wrong, please try again later !", text_type=["mono"], delme=3)
