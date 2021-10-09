import os
import asyncio

from sys import platform

from pyrogram.raw import functions
from pyrogram import filters, Client
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	error,
	gen,
	send_edit,
	long,
)




CMD_HELP.update(
	{"group" : (
		"group",
		{
		"group [group name]" : "Creates a basic group.",
		"sgroup [group name]" : "Creates a super group.",
		"unread" : "Mark a chat as unread in your telegram folders."
		}
		)
	}
)




@app.on_message(gen(["bgroup", "bgp"]))
async def create_basic_group(_, m: Message):
	if long(m) < 2:
		await send_edit(m, f"`Usage: {PREFIX}group [group name]`", delme=3)
		return
	args = m.text.split(None, 1)
	grpname = args[1]
	grptype = "basic"
	user_id = "@Alita_Robot"
	try:
		if grptype == "basic":
			try:
				await send_edit(
					m, 
					f"Creating a new basic group: `{grpname}`"
					)
				await app.create_group(f"{grpname}", user_id)
			except Exception as e:
				await error(m, e)
			await send_edit(m, f"**Created a new basic group:** `{grpname}`")
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["sgroup", "sgp"]))
async def create_supergroup(_, m: Message):
	if len(m.command) < 1:
		await send_edit(m, f"`Usage: {PREFIX}sgroup [group name]`", delme=3)
		return
	args = m.text.split(None, 1)
	grpname = args[1]
	grptype = "super"
	user_id = "@Alita_Robot"
	try:
		if grptype == "super":
			try:
				await send_edit(m, f"Creating a new super Group: `{grpname}`")
				await app.create_group(
					f"{grpname}", user_id
					)
			except Exception as e:
				await error(m, e)
			await send_edit(
				m, 
				f"**Created a new super Group:** `{grpname}`"
				)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["unread", "un"]))
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
		await error(m, e)




@app.on_message(gen("channel"))
async def create_channel(_, m: Message):
	if long(m) < 2:
		return await send_edit(m, f"`Usage: {PREFIX}channel [channel name]`", delme=3)

	chname = m.text.split(None, 1)[1]
	try:
		if chname:
			await send_edit(m, f"Creating your channel: `{chname}`")
			done = await app.create_channel(f"{chname}")
			if done:
				await send_edit(m, f"**Created channel:** `{chname}`")
			else:
				await send_edit(m, "Couldn't create a channel . . .")
	except Exception as e:
		await error(m, e)
		
		
		