import os, sys, time

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen, 
	error,
	send_edit,
)




CMD_HELP.update(
	{"power" : (
		"power",
		{
		"restart" : "restart userbot through sys.",
		"sleep [second]" : "sleep your userbot for a short duration.", 
		}
		)
	}
)




@app.on_message(gen("restart"))
async def restart_userbot(_, m: Message):
	try:
		msg = await send_edit(
			m, 
			"`Restarting bot ...`"
			)
		os.execv(sys.executable, ['python'] + sys.argv)
		await msg.edit(
			"Restart completed !\nBot is alive now !"
			)
	except Exception as e:
		await error(m, e)
		await m.edit(
			"`Failed to re-start userbot !`"
			)




# sleep 
@app.on_message(gen("sleep"))
async def sleep_userbot(_, m: Message):
	cmd = m.command[1]
	sleep = int(m.command[1])
	if cmd.isdigit() and sleep > 60 and sleep < 86400:
		one = int(cmd)
		sleeptime = int(one/60)
		suf = "minutes"
	else:
		sleeptime = cmd
		suf = "seconds"
	if cmd.isdigit():
		msg = await send_edit(
			m, 
			f"Sleeping for {sleeptime} {suf} ...")
		time.sleep(sleep)
		msg.delete()
	else:
		await send_edit(
			m, 
			"Please give me a number not text ..."
			)