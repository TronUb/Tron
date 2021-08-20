import os
import time
import asyncio

from telegraph import upload_file

from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_NAME,
	)

from tronx import telegraph as tgm

from tronx.helpers import (
	gen,
	error,
	send_edit,
)




if Config.USER_NAME:
	name = Config.USER_NAME
else:
	name = USER_NAME
NAME = str(name)


CMD_HELP.update( 
	{
		"telegraph": f"""
**PLUGIN:** `telegraph`\n\n
**COMMAND:** `{PREFIX}tgm «reply to message/media»` or `{PREFIX}telegraph «reply to message/media` \n\n**USAGE:** Reply To Media To Get Links Of That Media.\nSupported Media - (jpg, jpeg, png, gif, mp4)\n\n
"""
	} 
)




@app.on_message(gen(["tgm", "telegraph"]))
async def telegraph(app, m:Message):
	replied = m.reply_to_message
	filesize = 5242880
	# if not replied
	if not replied:
		await send_edit(
			m, 
			f"Please reply to media / text ...")
		return
	# replied to text 
	elif replied.text:
		if len(replied.text) <= 4096:
			await send_edit(
				m, 
				"⏳• Hold on..."
				)
			link = tgm.create_page(
				NAME,
				html_content=replied.text
				)
			await send_edit(
				m, 
				f"**Telegraph Link: [Press Here](https://telegra.ph/{link.get('path')})**",
				disable_web_page_preview=True
				)
		else:
			await send_edit(
				m, 
				"The length text exceeds 4096 characters ...")
	# replied to supported media
	elif replied.media:
		if (
			replied.photo and replied.photo.file_size <= filesize # png, jpg, jpeg
			or replied.video and replied.video.file_size <= filesize # mp4
			or replied.animation and replied.animation.file_size <= filesize
			or replied.sticker and replied.sticker.file_size <= filesize
			or replied.document and replied.document.file_size <= filesize # [photo, video] document
			):
			await send_edit(
				m, 
				"⏳• Hold on ..."
				)
			# change ext to png to use convert in link
			if replied.animation or replied.sticker:
				loc = await app.download_media(
					replied,
					file_name="app/tronx/downloads/telegraph.png"
					)
			else:
				loc = await app.download_media(
					replied, 
					file_name="app/tronx/downloads"
					)
			try:
				response = upload_file(loc)
			except Exception as e:
				await error(m, e)
			await send_edit(
				m, 
				f"**Telegraph Link: [Press Here](https://telegra.ph{response[0]})**", 
				disable_web_page_preview=True
				)
			os.remove(loc)
		else:
			await send_edit(
				m, 
				"Please check the file format or file size , it must be less than 5 mb ..."
				)
	else:
		# if replied to unsupported media
		await send_edit(
			m, 
			"`Sorry, The File is not supported !`"
			)
		time.sleep(2)
		await m.delete()


