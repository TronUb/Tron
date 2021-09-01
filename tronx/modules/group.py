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




@app.on_message(gen("bgroup"))
async def create_basicgroup(_, m: Message):
	if len(m.command) < 2:
		await send_edit(
			m, 
			f"`Usage: {PREFIX}group [group name]`"
			)
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
					f"Creating a Basic group: `{grpname}`"
					)
				await app.create_group(f"{grpname}", user_id)
			except Exception as e:
				await error(m, e)
				return
			await send_edit(
				m, 
				f"**Created new Basic group:** `{grpname}`"
				)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("sgroup"))
async def create_supergroup(_, m: Message):
	if len(m.command) < 1:
		await send_edit(
			m, 
			f"`Usage: {PREFIX}sgroup [group name]`"
			)
		return
	args = m.text.split(None, 1)
	grpname = args[1]
	grptype = "super"
	user_id = "@Alita_Robot"
	try:
		if grptype == "super":
			try:
				await send_edit(
					m, 
					f"Creating a Super Group: `{grpname}`"
					)
				await app.create_group(
					f"{grpname}", user_id
					)
			except Exception as e:
				await error(m, e)
				return
			await send_edit(
				m, 
				f"**Created new Super Group:** `{grpname}`"
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
					peer=await app.resolve_peer(m.chat.id), unread=True
				)
			),
		)
	except Exception as e:
		await error(m, e)
