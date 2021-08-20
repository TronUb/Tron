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
)




CMD_HELP.update(
    {
        "share": f"""
**PLUGIN:** `share`\n\n
**COMMAND:** `{PREFIX}send` \n**USAGE:** Send official plugin files from userbot to telegram chat.\n\n
**COMMAND:** `{PREFIX}install` \n**USAGE:** Reply to a .py file to install it in external modules directory.\n\n
**COMMAND:** `{PREFIX}uninstall «name of local plugin»` \nUSAGE:**  Uninstall Local installed modules.\n\n
"""
    }
)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.on_message(gen("send"))
async def send_modules(app, m: Message):
	await send_edit(
		m, 
		"`Checking...`"
		)
	if len(m.command) > 1:
		filename = m.text.split(None, 1)[1]
		modulename = f"tronx/modules/{filename}.py"
		if os.path.exists(modulename):
			thumb_image = await is_thumb_image_exists(
				modulename
				)
			if thumb_image:
				thumb_pic = thumb_image
			else:
				thumb_pic = Config.THUMB_PIC
			start = time.time()
			module_caption = os.path.basename(modulename)
			await send_edit(
				m, 
				f"Uploading {module_caption} ..."
				)
			try:
				await app.send_document(
					m.chat.id,
					document=modulename,
					thumb=thumb_pic,
					caption=(f"File name: `{module_caption}`\nUploaded By: `{mymention()}`"),
					parse_mode="markdown"
					)
			except Exception as e:
				await error(m, e)
				await send_edit(
					m, 
					"Look your Log chat for occurred error ..."
					)
			await m.delete()
		else:
			await send_edit(
				m, 
				"404: plugin not found ..."
				)
	else:
		await send_edit(
			m, 
			f"`{PREFIX}send <plugin name>`  to upload plugin file."
			)
		return




@app.on_message(gen("install"))
async def install_module(c: app, m: Message):
	if len(m.command) == 1 and m.reply_to_message.document:
		if m.reply_to_message.document.file_name.split(".")[-1] != "py":
			await send_edit(
				m, 
				"`Only (.py) modules can be installed !!`"
				)
			return
		module_loc = (
			f"/app/tronx/modules/{m.reply_to_message.document.file_name}"
		)
		await send_edit(
			m, 
			"`Installing module...`"
			)
		if os.path.exists(module_loc):
			await send_edit(
				m, 
				f"`Module **{m.reply_to_message.document.file_name}** already exists!`"
			)
			return
		try:
			download_loc = await c.download_media(
				message=m.reply_to_message, file_name=module_loc
			)
			if download_loc:
				await send_edit(
					m, 
					f"**Installed module:** `{m.reply_to_message.document.file_name}`"
				)
		except Exception as fail:
			await error(m, e)
	return




@app.on_message(gen("uninstall"))
async def uninstall_module(c: app, m: Message):
	if len(m.command) == 2:
		module_loc = f"/app/tronx/modules/{m.command[1]}.py"
		if os.path.exists(module_loc):
			os.remove(module_loc)
			await send_edit(
				m, 
				f"**Uninstalled module** {m.command[1]}"
				)
			return
		else:
			await send_edit(
				m,
				"`Module does not exist!`"
				)
			return
	else:
		await send_edit(
			m, 
			"`Enter a valid module name!`"
			)
		return
