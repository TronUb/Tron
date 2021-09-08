import os

from pyrogram.types import Message

from tronx import (
	app,
	USER_ID,
)

from tronx.helpers import (
	gen,
	send_edit,
)

from . import SUDO_USERS

from tronx.database.postgres import dv_sql as dv




@app.on_message(gen("addsudo"))
async def add_sudo(_, m: Message):
	replied = m.reply_to_message.from_user
	if not replied:
		await send_edit(
			m, 
			"Please reply to someone's message to add them in sudo list ..."
			)
		return
	else:
		if SUDO_USERS is None:
			sudo_id = [int(replied.id)]
			done = dv.setdv("SUDO_USERS", sudo_id)
			if done:
				await send_edit(m, f"Added {replied.first_name} in sudo list."
				)  
		elif SUDO_USERS != None:
			sudo_id = [int(dv.getdv("SUDO_USERS"))] + [int(replied.id)]
			done = dv.setdv("SUDO_USERS", sudo_id)
			if done:
				await send_edit(m, f"Added {replied.first_name} in sudo list."
				)
		else:
			await send_edit(m, "Currently i am unable to add this user in list . . ." 
			)