import os
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen, 
	error, 
	send_edit,
)




CMD_HELP.update(
	{
		"zombies": f"""
**PLUGIN:** `zombies`\n\n
**COMMAND:** `{PREFIX}zombies` \n**USAGE:** Get number of deleted accounts in a chat.\n
**COMMAND:** `{PREFIX}zombies clean` \n**USAGE:** Remove all deleted accounts from chat.\n
"""
	}
)




@app.on_message(gen("zombies"))
async def zombies_clean(_, m: Message):
	if m.chat.type == "private":
		await send_edit(m, "Please use this command in group ...")
		return
	if len(m.text.split()) != 2:
		await send_edit(
			m, 
			"`Checking deleted accounts ...`"
			)
		del_users = []
		async for x in app.iter_chat_members(chat_id=m.chat.id):
			if x.user.is_deleted:
				del_users.append(x.user.id)
		if del_users:
			await send_edit(
				m, 
				f"`Found {len(del_users)} Deleted accounts found!` Use `{PREFIX}zombies clean` to remove them from group."
			)
		else:
			await send_edit(
				m, 
				"`No deleted accounts found!\nGroup is clean as Hell!`"
				)
			await asyncio.sleep(1)
			await m.delete()
	elif len(m.text.split()) == 2 and m.text.split(None, 1)[1] == "clean":
		await send_edit(
			m, 
			"`Cleaning deleted accounts....`"
			)
		del_users = []
		u = 0
		async for x in app.iter_chat_members(chat_id=m.chat.id):
			await asyncio.sleep(0.1)
			if x.user.is_deleted:
				del_users.append(x.user.id)
				a = await app.get_chat_member(m.chat.id, x.user.id)
				if a.user.status not in ("administrator", "creator"):
					try:
						await app.kick_chat_member(m.chat.id, x.user.id)
						u += 1
						await asyncio.sleep(0.1)
					except:
						pass
		await send_edit(
			m, 
			f"Group clean-up done !\n`Removed {u} deleted accounts`"
			)
		await c.send_message(
			Config.LOG_CHAT,
			f"#ZOMBIES\nCleaned {len(del_users)} accounts from **{m.chat.title}** - `{m.chat.id}`",
		)
	else:
		await send_edit(
			m, 
			f"Check `{PREFIX}help zombies` to see how it works!"
		)
	return




