import os
import time
import shutil
import urllib

from requests import post

from pyrogram import Client
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
	PREFIX,
	)

from tronx.helpers import (
	error,
	mymention,
	gen,
	send_edit,
	# others 
	ReplyCheck,
	long,
)




CMD_HELP.update(
	{"carbon" : (
		"carbon",
		{
		"car [text]" : "Get a carbon imagw with written text on it.",
		"carbon [text]" : "Get a carbon image with written text on it"
		}
		)
	}
)




CARBON_LANG = "Auto"


colour_code = {
	"aqua": "rgba(0, 255, 255, 100)",
	"red": "rgba(255, 0, 0, 100)",
	"blue": "rgba(0, 0, 255, 100)",
	"green": "rgba(0, 255, 0, 100)",
	"yellow": "rgba(255, 255, 0, 100)",
	"gold": "rgba(255, 215, 0, 100)",
	"orange": "rgba(255, 165, 0, 100)",
	"purple": "rgba(41, 5, 68, 100)",
	"black": "rgba(0, 0, 0, 100)",
	"white": "rgba(255, 255, 255, 100)",
	"lime": "rgba(0, 255, 0, 100)",
	"silver": "rgba(192, 192, 192, 100)",
	"maroon": "rgba(128, 0, 0, 100)",
	"olive": "rgba(128, 128, 0, 100)",
	"teal": "rgba(0, 128, 128, 100)",
	"navy": "rgba(0, 128, 128, 100)",
	"choclate": "rgba(210, 105, 30, 100)",
}




@app.on_message(gen(["carbon", "carb"]))
async def carb_api(_, m: Message):
	cmd = m.command
	if long(m) < 2:
		await send_edit(
			m, 
			f"Usage:\n\n1) `{PREFIX}carbon [colour] [text]`\n2) `{PREFIX}carbon [text]`\n\n**Note:** Default colour aqua",
			delme=2
			)
		return

	elif long(m) <= 4096:
		try:
			await send_edit(
				m, 
				"creating carbon..."
				)
			if cmd[1] in colour_code:
				text = m.text.split(None, 2)[2]
				colour = cmd[1]
				await create_carbon(app, m, text=text, colour=colour)
			else:
				text = m.text.split(None, 1)[1]
				colour= "aqua"
				await create_carbon(
					app, 
					m, 
					text=text, 
					colour=colour
					)
		except Exception as e:
			await error(m, e)
	elif long(m) > 4096:
		await send_edit(
			m, 
			"Something went wrong !"
			delme=2
			)




@app.on_message(gen("carblist"))
async def carb_colour_list(_, m: Message):
	clist = list(colour_code.keys())
	await send_edit(
		m,
		"\n".join(clist)
		)




async def create_carbon(app: Client, m: Message, text, colour):
	json = {"backgroundColor": f"{colour_code.get(colour)}",
		"theme": "Dracula",
		"exportSize": "4x",}
	json["code"] = urllib.parse.quote(text)
	json["language"] = CARBON_LANG
	apiUrl = "http://carbonnowsh.herokuapp.com"
	text = post(apiUrl, json=json, stream=True)
	filename = "carbon_image.png"
	if text.status_code == 200:
		text.raw.decode_content = True
		with open(filename, "wb") as f:
			shutil.copyfileobj(text.raw, f)
			f.close()
		await app.send_document(
			m.chat.id,
			filename,
			caption=f"**Carbon Made by:** {mymention()}",
			reply_to_message_id=ReplyCheck(m),
		)
		await m.delete()
	else:
		await send_edit(
			m, 
			"Image Couldn't be retreived . . .",
			delme=2
			)
		time.sleep(2)
		await m.delete()
	os.remove(filename)