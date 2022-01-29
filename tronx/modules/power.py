import os
import sys

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen, 
)




app.CMD_HELP.update(
	{"power" : (
		"power",
		{
		"restart" : "restart userbot through sys.",
		"sleep [second]" : "sleep your userbot for a short duration.", 
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




# sleep 
@app.on_message(gen("sleep"))
async def sleep_userbot(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Give me some seconds after command . . .")

	elif app.long(m) > 1:
		cmd = int(m.command[1])

	if cmd.isdigit():
		if int(cmd) > 60:
			sleeptime = int(cmd//60)
			sec = "minutes"
		elif int(cmd) < 60:
			sleeptime = int(cmd)
			sec = "seconds"
		elif int(cmd) > 3600:
			sleeptime = int(cmd//3600)
			sec = "hours"
		elif int(cmd) > 86400:
			return await app.send_edit(m, "Sorry you can't sleep bot for more than 24 hours . . .", delme=3)
		else:
			return

		await app.send_edit(m, f"Sleeping for {sleeptime} {sec} ...", delme=int(cmd))
		time.sleep(int(cmd))
	else:
		await app.send_edit(m, "Please give me a number not text ...", delme=2, mono=True)
