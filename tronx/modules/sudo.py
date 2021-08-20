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




@app.on_message(gen("addsudo"))
async def add_sudo(_, m: Message):
	replied = m.reply_to_message
	if not replied:
		await send_edit(
			m, 
			"Please reply to someone's message to add them in sudo list ..."
			)
		return
	else:
		sudos = os.environ.get("SUDO_USERS")
		if sudos == None:
			os.environ["SUDO_USERS"] = str([replied.from_user.id])
		else:
			os.environ["SUDO_USERS"] = str([sudos, replied.from_user.id])
		await send_edit(m, f"Added {replied.from_user.first_name} as sudo !")