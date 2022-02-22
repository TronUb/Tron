import os
import asyncio

from pyrogram.raw import functions
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




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




@app.on_message(gen(["bgroup", "bgp"], allow_sudo=True))
async def create_basic_group(_, m: Message):
	if app.long(m) < 2:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}bgroup [group name]`", delme=3)

	args = m.text.split(None, 1)
	grpname = args[1]
	grptype = "basic"
	user_id = "@Alita_Robot"
	try:
		m = await app.send_edit(m, f"Creating a new basic group: `{grpname}`")
		groupjson = await app.create_group(f"{grpname}", user_id)
		await app.send_edit(m, f"**Created a new basic group:** `{grpname}`")
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["sgroup", "sgp"], allow_sudo=True))
async def create_supergroup(_, m: Message):
	if len(m.command) < 1:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}sgroup [group name]`", delme=3)

	args = m.text.split(None, 1)
	grpname = args[1]
	grptype = "super"
	user_id = "@Alita_Robot"
	try:
		m = await app.send_edit(m, f"Creating a new super Group: `{grpname}`")
		await app.create_supergroup(f"{grpname}", user_id)
		await app.send_edit(m, f"**Created a new super Group:** `{grpname}`")
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["unread", "un"], allow_sudo=True))
async def mark_chat_unread(_, m: Message):
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




@app.on_message(gen("channel", allow_sudo=True))
async def create_channel(_, m: Message):
	if app.long(m) < 2:
		return await app.send_edit(m, f"`Usage: {app.PREFIX}channel [channel name]`", delme=3)

	chname = m.text.split(None, 1)[1]
	try:
		if chname:
			m = await app.send_edit(m, f"Creating your channel: `{chname}`")
			done = await app.create_channel(f"{chname}")
			if done:
				await app.send_edit(m, f"**Created channel:** `{chname}`")
			else:
				await app.send_edit(m, "Couldn't create a channel . . .")
	except Exception as e:
		await app.error(m, e)
		
		
		
