from pyrogram.types import Message
from tronx import app



@app.on_message(gen("addsudo"))
async def add_sudo(_, m: Message):
	reply = m.reply_to_message

	if not reply:
		return await app.send_edit(m, "Reply to a user to add him in sudo list", mono=True, delme=4)  

	sudo_list = app.getdv("SUDO_USERS")
	if sudo_list:
		all_sudo = [x for x in sudo_list.split()] + [str(reply.from_user.id)]
	else:
		all_sudo = [str(reply.from_user.id)]

	app.setdv("SUDO_USERS", " ".join(all_sudo))
	await app.send_edit(m, f"{reply.from_user.mention()} `has been added to sudo.`", delme=4)


