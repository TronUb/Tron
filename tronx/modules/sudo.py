from pyrogram.types import Message
from tronx.helpers import gen
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

	app.setdv("SUDO_USERS", " ".join(list(set(all_sudo)))) # rem duplicates
	await app.send_edit(m, f"{reply.from_user.mention()} `has been added to sudo.`", delme=4)




@app.on_message(gen("getsudo"))
async def get_sudo(_, m: Message):
	sudo_list = [x for x in app.getdv("SUDO_USERS").split()]
	await app.send_edit(m, "**Available Sudo id:**\n\n" + "\n".join(sudo_list))




@app.on_message(gen("delsudo"))
async def get_sudo(_, m: Message):
	reply = m.reply_to_message
	user_id = str(reply.from_user.id)
	if not reply:
		return await app.send_edit(m, "Reply to a user to add him in sudo list", mono=True, delme=4)  

	sudo_list = [x for x in app.getdv("SUDO_USERS").split()]
	if user_id in sudo_list:
		sudo_list.remove(user_id)
	else:
		return await app.send_edit(m, "This user is not in sudo list", mono=True, delme=4)

	await app.send_edit(m, f"{reply.from_user.mention()} `has been removed from sudo list`", delme=4)


