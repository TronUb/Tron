import os
import sys
import time
import asyncio

from pyrogram import filters, Client
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
	USER_NAME, 
	USER_ID,
	Config,
	PREFIX
	)
from tronx.helpers import (
	error,
	mymention,
	gen,
	send_edit,
	create_file,
)




CMD_HELP.update(
	{"dict" : (
		"dict",
		{
		"new [file name]" : "Create a python file with your codes."
		}
		)
	}
)




@app.on_message(gen("new"))
async def create_anyfile(app, m:Message):
	await send_edit(
		m, 
		"making file ..."
		)
	cmd = m.command
	if (len(cmd) < 4096) and (len(cmd) > 2):
		try:
			data = " ".join(cmd[1:])
			givename = cmd[1]
			await create_file(
				m, 
				app, 
				filename=givename, 
				text=data
				)
			return
		except Exception as e:
			await error(m, e)
	# if replied to text without file name
	elif (len(cmd) == 1) and m.reply_to_message:
		try:
			data = m.reply_to_message.text
			await create_file(
				m, 
				app, 
				filename="file.py", 
				text=data
				)
			return
		except Exception as e:
			await error(m, e)
	# if replied to text with file name
	elif (len(cmd) == 2) and m.reply_to_message:
		try:
			givename = cmd[1]
			data = m.reply_to_message.text
			await create_file(
				m, 
				app, 
				filename=givename, 
				text=data
				)
			return
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			f"Use cmd correctly: `{PREFIX}new [ file name ]`\n\nNote: use filename with extention, ex: file.py"
			)



