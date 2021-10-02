import os, sys

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
	reply = m.reply_to_message.from_user
	users = dv.getdv("SUDO_USERS")
	user_id = str(reply.id)

	if not m.reply_to_message:
		await send_edit(
			m, 
			"Please reply to someone's message to add them in sudo list . . .",
			mono=True
			)
	else:
		if bool(users) is True:
			if not str(users).startswith("["):
				users = [users]
			sudo_id = [user_id] + users
			done = dv.setdv("SUDO_USERS", sudo_id)
			if done:
				msg = await send_edit(
					m, 
					f"Added {reply.first_name} to sudo, bot is rebooting wait a minute . . . ",
					mono=True
					)
				os.execv(sys.executable, ['python'] + sys.argv)
				await app.edit_message_text(
					m.chat.id, 
					msg.message_id,
					f"Reboot completed !"
					)
			elif not done:
				await send_edit(m, "Failed to add sudo !", mono=True)
		else:
			dv.setdv("SUDO_USERS", [user_id])
			await send_edit(
				m, 
				f"Added {reply.first_name} to sudo, bot is rebooting wait a minute . . . ",
				mono=True
					)
			os.execv(sys.executable, ['python'] + sys.argv)
			await send_edit(
				m, 
				f"Reboot completed !"
				)




@app.on_message(gen("getsudo"))
async def get_sudos(_, m):
	await send_edit(m, "Just a second . . .", mono=True)
	if bool(dv.getdv("SUDO_USERS")) is True:
		users = dv.getdv("SUDO_USERS")
		stored = []
		for user in users:
			data = await app.get_users(user)
			stored.append(data.first_name)

		await send_edit(m, "\n".join(stored))
	else:
		await send_edit(m, "There are no sudo users . . .", mono=True)




@app.on_message(gen("delsudo"))
async def delete_sudo(_, m):
	reply = m.reply_to_message
	users = int(dv.getdv("SUDO_USERS"))
	if not reply:
		await send_edit(m, "Atleast reply the sudo user to remove from sudo users . . .", mono=True)  
	elif reply:
		if bool(users) is True:
			if reply.from_user.id in [users]:
				users.remove(reply.from_user.id)
				dv.setdv("SUDO_USERS", users)
				await send_edit(m, f"{reply.first_name} is now removed from sudo list.", mono=True)
			else:
				await send_edit(m, "This user is not in sudo list.", mono=True)
		else:
			await send_edit(m, "Sorry you haven't added any sudo users in sudo list.", mono=True)
	else:
		await send_edit(m, "Program failed.")
				