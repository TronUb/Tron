import time

from tronx.database.postgres import dv_sql as db

from pyrogram.types import Message

from tronx import (
	app,
	CMD_HELP,
)

from tronx.helpers import (
	gen,
	long,
	send_edit,
	error,
)




CMD_HELP.update(
	{"download" : (
		"download",
		{
		"setdv [varname] [value]" : "Set any database vars, for ex: .setdv [USER_NAME] [BEAST]",
		"getdv [varname]" : "Get a existing database vars value.",
		"deldv [varname]" : "Delete a existing database var with its value.",
		}
		)
	}
)



@app.on_message(gen("setdv"))
async def set_dv_var(_, m: Message):
	if long(m) == 2:
		await send_edit(m, "Please give me key with a value . . . ", delme=2)  
		return
	if long(m) > 2 and long(m) < 4096:
		key = m.command[1]
		value = m.text.split(None, 2)[2]
		done = db.setdv(key, value)
		if done:
			await send_edit(m, f"Added database var with key = `{key}` and value = `{value}`")

		elif not done:
			await send_edit(m, "Failed to a add key & value to database var . . .", delme=2)

	else:
		await send_edit(m, "Maximum 4096 characters in one message . . .", delme=2)




@app.on_message(gen("deldv"))
async def del_dv_var(_, m: Message):
	if long(m) == 1:
		await send_edit(m, "Give me some key to delete that a var from database . . . ", delme=2)

	elif long(m) > 1:
		key = m.command[1]
		done = db.deldv(key)
		await send_edit(m, f"Successfully deleted key = `{key}`")

	else:
		await send_edit(m, "Maximum 4096 characters in one message . . .", delme=2)




@app.on_message(gen("getdv"))
async def get_dv_var(_, m: Message):
	if long(m) == 1:
		await send_edit(m, "Give me some key to get value that a var from database . . . ", delme=2)

	elif long(m) > 1:
		key = m.command[1]
		done = db.getdv(key)
		if done:
			await send_edit(m, f"Here:\n\nkey = `{key}`\n\nvalue = `{done}`")

		elif not done:
			await send_edit(m, "This var doesn't exist in my database . . .", delme=2)
	else:
		await send_edit(m, "Maximum 4096 characters in one message . . .", delme=2)




@app.on_message(gen("pm"))
async def get_dv_var(_, m: Message):
	arg = m.command
	if long(m) < 2:
		await send_edit(
			m, 
			"Provide me a suffix to do some work\n\nSuffix: `on` & `off`"
			)
	elif long(m) is > 1 and arg[1] = "on":
		if bool(dv.getdv("PMPERMIT")) is True:
			await send_edit(
				m, 
				"Pmguard is already active !"
				)
		elif bool(dv.getdv("PMPERMIT")) is False:
			dv.setdv("PMPERMIT", "True")
			await send_edit(
				m, 
				"Pmguard is now turned on !"
				)
	elif long(m) > 1 and arg[1] == "off":
		dv.deldv("PMPERMIT")
		await send_edit(
			m, 
			"Pmguard is now turned off !"
			)
	elif long(m) > 1 and arg[1] not in ["on", "off"]:
		await send_edit(
			m, 
			"Use `on` or `off` after command to turn on & off pmguard !"
			)