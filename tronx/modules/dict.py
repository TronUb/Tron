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
	long,
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
	reply = m.reply_to_message
	await send_edit(m, "making file ...")
	cmd = m.command
	try:
		if long(m) < 4096 and long(m) > 2:
			data = " ".join(cmd[1:])
			givename = cmd[1]
			await create_file(
				m, 
				filename=givename, 
				text=data
			)
		# if replied to text without file name
		elif long(m) == 1 and reply:
			data = reply.text
			await create_file(
				m, 
				filename="file.py", 
				text=data
			)
		# if replied to text with file name
		elif long(m) > 1 and reply:
			givename = cmd[1]
			data = reply.text
			await create_file(
				m, 
				filename=givename, 
				text=data
			)
		else:
			await send_edit(
				m, 
				f"Use cmd correctly: `{PREFIX}new [ file name ] [content]`\n\nNote: use filename with extention, ex: file.py, file.txt, etc",
				)
	except Exception as e:
		await error(m, e)


