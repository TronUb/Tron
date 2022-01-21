import os
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen, 
	error, 
	send_edit,
	private,
	long,
)




app.CMD_HELP.update(
	{"zombies" : (
		"zombies",
		{
		"zombies" : "Get number of deleted accounts in a chat.",
		"zombies clean" : "Remove all deleted accounts from chat."
		}
		)
	}
)




@app.on_message(gen("zombies"))
async def remove_deleted(_, m: Message):
	await private(m)

	temp_count = 0
	admin_count = 0
	count = 0

	if long(m) != 2:
		await send_edit(m, "Checking deleted accounts . . .", mono=True)

		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted:
				temp_count += 1

		if temp_count > 0:
			await send_edit(m, f"Found `{temp_count}` Deleted accounts found! Use `{app.PREFIX}zombies clean` to remove them from group.")
		else:
			await send_edit(m, "No deleted accounts found.\nGroup is clean as Hell ! 😃", delme=3, mono=True)

	elif long(m) == 2 and m.command[1] == "clean":
		await send_edit(m, "Cleaning deleted accounts . . .", mono=True)

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
					await error(m, e)
		await send_edit(m, f"`Group clean up done !`\n\n**Total:** `{count+admin_count}`\n**Removed:** `{count}`\n**Not Removed:** `{admin_count}`\n\n**Note:** `Not removed accounts can be admins or the owner`")

	elif long(m) == 2 and m.command[1] != "clean":
		await send_edit(m, f"Check `{app.PREFIX}help zombies` to see how it works !")
	else:
		await send_edit(m, "Something went wrong, please try again later !", mono=True, delme=3)




