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
	if not m.reply_to_message:
		await send_edit(
			m, 
			"Please reply to someone's message to add them in sudo list ..."
			)
		return
	else:
		if SUDO_USERS is not None and bool(dv.getdv("SUDO_USERS")) is True:
			sudo_id = [int(replied.id)] + [int(dv.getdv("SUDO_USERS"))]
			done = dv.setdv("SUDO_USERS", sudo_id)
			if done:
				await send_edit(
					m, f"Added {replied.first_name} to sudo !"
					)
			elif not done:
				await send_edit(m, "Failed to add sudo !")
