import asyncio

from pyrogram.raw import functions
from pyrogram.types import Message

from tronx import app, gen




app.CMD_HELP.update(
	{"group" : (
		"group",
		{
		"bgroup [group name]" : "Creates a basic group.",
		"sgroup [group name]" : "Creates a super group.",
		"unread" : "Mark a chat as unread in your telegram folders.",
		"channel [channel name]" : "Create a channel through this command."
		}
		)
	}
)




@app.on_message(gen(["bgroup", "bgp"], allow =["sudo"]))
async def basicgroup_handler(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}bgroup mygroupname`", delme=4)
	elif app.long(m) > 1:
		grpname = m.text.split(None, 1)[1]
		about = ""
	elif app.long(m) > 2:
		grpname = m.text.split(None, 1)[1]
		about = m.text.split(None, 2)[2]
	else:
		grpname = False
		about = ""

	try:
		if grpname:
			m = await app.send_edit(m, f"Creating a new basic group: `{grpname}`")
			group = await app.create_group(title=f"{grpname}", description=about)
			await app.send_edit(m, f"**Created a new super Group:** [{grpname}]({(await app.get_chat(group.id)).invite_link})")
		else:
			await app.send_edit(m, "No group name is provided.", text_type=["mono"], delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["sgroup", "sgp"], allow =["sudo"]))
async def supergroup_handler(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}sgroup mygroupname`", delme=4)
	elif app.long(m) > 1:
		grpname = m.text.split(None, 1)[1]
		about = ""
	elif app.long(m) > 2:
		grpname = m.text.split(None, 1)[1]
		about = m.text.split(None, 2)[2]
	else:
		grpname = False
		about = ""

	try:
		if grpname:
			m = await app.send_edit(m, f"Creating a new super group: `{grpname}`")
			group = await app.create_supergroup(title=f"{grpname}", description=about)
			await app.send_edit(m, f"**Created a new super Group:** [{grpname}]({(await app.get_chat(group.id)).invite_link})")
		else:
			await app.send_edit(m, "No group name is provided.", text_type=["mono"], delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["unread", "un"], allow =["sudo"]))
async def unreadchat_handler(_, m: Message):
	try:
		await asyncio.gather(
			m.delete(),
			app.send(
				functions.messages.MarkDialogUnread(
					peer=await app.resolve_peer(m.chat.id), 
					unread=True
				)
			),
		)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("channel", allow =["sudo"]))
async def channel_handler(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}channel [channel name]`", delme=4)

	elif app.long(m) > 1:
		chname = m.text.split(None, 1)[1]
		about = ""
	elif app.long(m) > 2:
		chname = m.text.split(None, 1)[1]
		about = m.text.split(None, 2)[2]

	try:
		if chname:
			m = await app.send_edit(m, f"Creating your channel: `{chname}`")
			response = await app.create_channel(title=f"{chname}", description=about)
			if response:
				await app.send_edit(m, f"**Created channel:** [{chname}]({(app.get_chat(response.id)).invite_link})", disable_web_page_preview=True)
			else:
				await app.send_edit(m, "Couldn't create a channel.")
	except Exception as e:
		await app.error(m, e)
