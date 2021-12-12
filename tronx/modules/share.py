import re
import os
import time
import asyncio

from datetime import datetime

from pyrogram import errors
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_ID,
	USER_NAME
	)

from tronx.helpers import (
	gen,
	error,
	mymention,
	send_edit,
	# others 
	is_thumb_image_exists, 
	mention_markdown,
	long,
	aexec,
)

from tronx.database.postgres import dv_sql as dv




CMD_HELP.update(
	{"share" : (
		"share",
		{
		"send [plugin name]" : "Send official plugin files from userbot to telegram chat.",
		"install [reply to plugin]" : "Reply to a .py file to install it in external modules directory.",
		"uninstall [name of local plugin]" : "Uninstall Local installed modules."
		}
		)
	}
)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("send"))
async def send_modules(app, m: Message):
	await send_edit(m, "`Checking...`")
	if len(m.command) > 1:
		filename = m.text.split(None, 1)[1]
		modulename = f"tronx/modules/{filename}.py"
		if os.path.exists(modulename):
			thumb_image = await is_thumb_image_exists(
				modulename
				)

			if thumb_image:
				thumb_pic = thumb_image
			elif dv.getdv("THUMB_PIC"):
				thumb_pic = dv.getdv("THUMB_PIC")
			else:
				thumb_pic = Config.THUMB_PIC

			start = time.time()
			module_caption = os.path.basename(modulename)
			await send_edit(m, f"Uploading {module_caption} . . .")

			try:
				await app.send_document(
					m.chat.id,
					document=modulename,
					thumb=thumb_pic,
					caption=(f"File name: `{module_caption}`\n\nUploaded By: {mymention()}")
					)
			except Exception as e:
				await error(m, e)
				await send_edit(m, "Try again later, check log chat . . .", delme=2)
		else:
			await send_edit(m, "`404: plugin not found . . .`", delme=2)
	else:
		await send_edit(m, f"`{PREFIX}send <plugin name>`  to upload plugin file.", delme=2)
	return




@app.on_message(gen("install"))
async def install_module(_, m: Message):
	if long(m) == 1 and m.reply_to_message.document:
		if not m.reply_to_message.document.file_name.endswith(".py"):
			return await send_edit(m, "`Only (.py) modules can be installed !!`", delme=2)
		reply = m.reply_to_message
		doc_name = reply.document.file_name

		module_loc = (
			f"tronx/modules/{doc_name}"
		)
		await send_edit(m, "Installing module . . .", delme=2, mono=True)
		if os.path.exists(module_loc):
			return await send_edit(m, f"Module `{doc_name}` already exists ! skipping installation !", delme=5)

		try:
			download_loc = await app.download_media(
				message=reply, 
				file_name=module_loc
			)
			if download_loc:
				await send_edit(m, f"**Installed module:** `{doc_name}`")
				data = open(download_loc, "r")
				await aexec(data.read())
			else:
				await send_edit(m, f"Failed to install module {doc_name}", mono=True, delme=4)
		except Exception as e:
			await error(m, e)




@app.on_message(gen("uninstall"))
async def uninstall_module(_, m: Message):
	cmd = m.command
	try:
		if long(m) > 1:
			if cmd[1].endswith(".py"):
				module_loc = f"tronx/modules/{cmd[1]}"
			elif not cmd[1].endswith(".py"):
				module_loc = f"tronx/modules/{cmd[1]}.py"
			if os.path.exists(module_loc):
				os.remove(module_loc)
				await send_edit(m, f"**Uninstalled module** {cmd[1]}")
			else:
				await send_edit(m,"Module does not exist!", delme=2, mono=True)
		else:
			await send_edit(m, "Give me a module name . . .", mono=True)
	except Exception as e:
		await error(m, e)
