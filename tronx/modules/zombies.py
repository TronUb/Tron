import os
import asyncio

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen, 
)




app.CMD_HELP.update(
	{"zombies" : (
		"zombies",
		{
		"zombies" : "Get number of deleted accounts in a chat.",
		"zombies [clean]" : "Remove all deleted accounts from chat."
		}
		)
	}
)




@app.on_message(gen("zombies"))
async def remove_deleted(_, m: Message):
	await app.private(m)

	temp_count = 0
	admin_count = 0
	count = 0

	if app.long(m) != 2:
		m = await app.send_edit(m, "Checking deleted accounts . . .", mono=True)

		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted:
				temp_count += 1

		if temp_count > 0:
			await app.send_edit(m, f"**Found:** `{temp_count}` Deleted accounts\nUse `{app.PREFIX}zombies clean` to remove them from group.")
		else:
			await app.send_edit(m, "No deleted accounts found.\nGroup is clean as Hell ! 😃", delme=3, mono=True)

	elif app.long(m) == 2 and m.command[1] == "clean":
		m = await app.send_edit(m, "Cleaning deleted accounts . . .", mono=True)

		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted:
				if x.status in ("administrator", "creator"):
					admin_count += 1
					continue
				try:
					await app.kick_chat_member(m.chat.id, x.user.id)
					count += 1
					await asyncio.sleep(0.2)
				except Exception as e:
					await app.error(m, e)
		await app.send_edit(m, f"`Group clean up done !`\n\n**Total:** `{count+admin_count}`\n**Removed:** `{count}`\n**Not Removed:** `{admin_count}`\n\n**Note:** `Not removed accounts can be admins or the owner`")

	elif app.long(m) == 2 and m.command[1] != "clean":
		await app.send_edit(m, f"Check `{app.PREFIX}help zombies` to see how it works !")
	else:
		await app.send_edit(m, "Something went wrong, please try again later !", mono=True, delme=3)




