import os
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	)

from tronx.helpers import (
	gen, 
	error, 
	send_edit,
	private,
	long,
)




CMD_HELP.update(
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
async def zombies_clean(_, m: Message):
	await private(m)
	del_users = []
	del_users.clear()

	if long(m) != 2:
		await send_edit(m, "Checking deleted accounts . . .",mono=True)

		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted:
				del_users.append(x.user.id)
		if bool(del_users) is True:
			await send_edit(m, f"Found {len(del_users)} Deleted accounts found! Use `{PREFIX}zombies clean` to remove them from group.")
		else:
			await send_edit(m, "No deleted accounts found!\nGroup is clean as Hell!", delme=2, mono=True)

	elif long(m) == 2 and m.command[1] == "clean":
		await send_edit(m, "Cleaning deleted accounts . . .",mono=True)

		count = 0
		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted and x.status not in ("administrator", "creator"):
					try:
						await app.kick_chat_member(m.chat.id, x.user.id)
						count += 1
						await asyncio.sleep(0.1)
					except Exception as e:
						await error(m, e)
		if count == 0:
			await send_edit(m, f"Group clean-up done !\nFailed to remove deleted accounts (maybe they are admins)")
		else:
			await send_edit(m, f"Group clean-up done !\nRemoved `{count}` deleted accounts in {m.chat.title}.")

	else:
		await send_edit(m, f"Check `{PREFIX}help zombies` to see how it works!")




