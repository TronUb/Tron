import re
import os
import time

from datetime import datetime

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
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


@app.on_message(gen("send", allow = ["sudo", "channel"]))
async def send_modules(app, m: Message):
	await app.send_edit(m, "`Checking...`")
	if app.long(m) > 1:
		filename = m.command[1]
		modulename = f"tronx/modules/{filename}.py"
		if os.path.exists(modulename):
			thumb_image = await app.IsThumbExists(modulename)

			if thumb_image:
				thumb_pic = thumb_image
			elif app.getdv("THUMB_PIC"):
				thumb_pic = app.getdv("THUMB_PIC")
			else:
				thumb_pic = app.THUMB_PIC

			start = time.time()
			module_caption = os.path.basename(modulename)
			await app.send_edit(m, f"Uploading {module_caption} . . .")

			try:
				await app.send_document(
					m.chat.id,
					document=modulename,
					thumb=thumb_pic,
					caption=(f"File name: `{module_caption}`\n\nUploaded By: {app.UserMention()}")
					)
			except Exception as e:
				await app.error(m, e)
				await app.send_edit(m, "Try again later, check log chat . . .", delme=3)
		else:
			await app.send_edit(m, "404: plugin not found . . .", delme=2, text_type=["mono"])
	else:
		await app.send_edit(m, f"`{app.PREFIX}send [ plugin name ]`  to upload plugin file.", delme=3)




@app.on_message(gen("install"))
async def install_module(_, m: Message):
	reply = m.reply_to_message
	if not reply:
		return await app.send_edit(m, "Reply to a python file to install . . .", text_type=["mono"], delme=4)
	if reply:
		if not reply.document.file_name.endswith(".py"):
			return await app.send_edit(m, "Only (.py) modules can be installed !!", text_type=["mono"], delme=2)
		doc_name = reply.document.file_name

		module_loc = (
			f"tronx/modules/{doc_name}"
		)
		await app.send_edit(m, "Installing module . . .", text_type=["mono"])
		if os.path.exists(module_loc):
			return await app.send_edit(m, f"Module `{doc_name}` already exists ! skipping installation !", delme=5)

		try:
			download_loc = await app.download_media(
				message=reply, 
				file_name=module_loc
			)
			if download_loc:
				await app.send_edit(m, f"**Installed module:** `{doc_name}`", delme=5)
				data = open(download_loc, "r")
				await app.aexec(m, data.read())
			else:
				await app.send_edit(m, f"Failed to install module {doc_name}", text_type=["mono"], delme=4)
		except Exception as e:
			await app.error(m, e)





@app.on_message(gen("uninstall"))
async def uninstall_module(_, m: Message):
	cmd = m.command
	try:
		if app.long(m) > 1:
			if cmd[1].endswith(".py"):
				module_loc = f"tronx/modules/{cmd[1]}"
			elif not cmd[1].endswith(".py"):
				module_loc = f"tronx/modules/{cmd[1]}.py"
			if os.path.exists(module_loc):
				os.remove(module_loc)
				await app.send_edit(m, f"**Uninstalled module:** {cmd[1]}", delme=5)
			else:
				await app.send_edit(m,"Module doesn't exist !", delme=4, text_type=["mono"])
		else:
			await app.send_edit(m, "Give me a module name . . .", text_type=["mono"], delme=4)
	except Exception as e:
		await app.error(m, e)
