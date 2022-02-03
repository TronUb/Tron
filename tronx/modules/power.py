import os
import sys
import time
import asyncio

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen, 
)




app.CMD_HELP.update(
	{"power" : (
		"power",
		{
		"reboot" : "restarts the userbot through sys. (not heroku)",
		"sleep [seconds]" : "The bot sleeps with your desired given input.\n**Note:** input must be less than <= 86400 seconds", 
		}
		)
	}
)




@app.on_message(gen("reboot"))
async def restart_userbot(_, m: Message):
	try:
		msg = await app.send_edit(m, "`Restarting bot ...`")

		os.execv(sys.executable, ['python'] + sys.argv)
		await app.edit_message_text(
			msg.chat.id,
			msg.message_id,
			"Restart completed !\nBot is alive now !"
		)
	except Exception as e:
		await m.edit("Failed to restart userbot !", delme=2, mono=True)
		await app.error(m, e)




@app.on_message(gen("sleep"))
async def sleep_userbot(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Give me some seconds after command . . .")

	elif app.long(m) > 1:
		arg = m.command[1]

	if arg.isdigit():
		cmd = int(arg)
		if cmd > 86400:
			return await app.send_edit(m, "Sorry you can't sleep bot for more than 24 hours (> 86400 seconds) . . .", mono=True, delme=3)

		format = {
			cmd<60:f"{cmd} seconds", 
			cmd>=60:f"{cmd//60} minutes", 
			cmd>=3600:f"{cmd//3600} hours"
			}

		suffix = "`null`"
		for x in format.keys(): # very small loop
			if x:
				suffix = format[x]
				break

		await app.send_edit(m, f"Sleeping for {suffix} . . .", delme=cmd)
		time.sleep(cmd) 
	else:
		await app.send_edit(m, "Please give me a number not text . . .", delme=3, mono=True)
