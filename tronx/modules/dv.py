import time

from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)

from config import Config





app.CMD_HELP.update(
	{"dv" : (
		"dv",
		{
		"setdv [varname] [value]" : "Set any database vars, for ex: .setdv [USER_NAME] [BEAST]",
		"getdv [varname]" : "Get a existing database vars value.",
		"deldv [varname]" : "Delete a existing database var with its value.",
		"alldv" : "Get all existing database vars.",
		"pm [on | off]" : "Turn on & off your pmguard",
		}
		)
	}
)



@app.on_message(gen("setdv", allow =["sudo"]))
async def setdv_handler(_, m: Message):
	if app.long(m) == 1:
		allvars = [f"`{x}`" for x in dir(Config) if x.isupper()]
		await app.send_edit(m, "**AVAILABLE DB VARS:**\n\n" + "\n".join(allvars))

	elif app.textlen(m) > 4096:
		await app.send_edit(m, "Text is too long. only 4096 characters are allowed.", mono=True, delme=4)

	elif app.long(m) == 2:
		await app.send_edit(m, "Please give me key with a value.", mono=True, delme=4)  

	elif app.long(m) > 2:
		key = m.command[1]
		value = m.text.split(None, 2)[2]
		done = app.setdv(key, value)

		if done:
			await app.send_edit(m, f"Added database var with [ **key** = `{key}` ] and [ **value** = `{value}` ]")

		elif not done:
			await app.send_edit(m, "Failed to a add key & value to database var.", mono=True, delme=2)




@app.on_message(gen("deldv", allow =["sudo"]))
async def deldv_handler(_, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Give me some key to delete that a var from database . . . ", mono=True, delme=2)

	elif app.textlen(m) > 4096:
		await app.send_edit(m, "text is too long. only 4096 characters are allowed.", mono=True, delme=4)

	elif app.long(m) > 1:
		key = m.command[1]
		done = app.deldv(key)

		await app.send_edit(m, f"Successfully deleted [ **key** = `{key}` ]", delme=4)
	else:
		await app.send_edit(m, "Something went wrong, try again later !", mono=True, delme=4)



@app.on_message(gen("getdv", allow =["sudo"]))
async def getdv_handler(_, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Give me some key to get value that a var from database . . . ", mono=True, delme=2)

	elif app.long(m) > 1:
		key = m.command[1]
		done = app.getdv(key)

		if done:
			await app.send_edit(m, f"**Here:**\n\n**key** = `{key}`\n\n**value** = `{done}`", delme=4)
		else:
			await app.send_edit(m, "This var doesn't exist in my database.", mono=True, delme=4)
	else:
		await app.send_edit(m, "Maximum 4096 characters in one message . . .", mono=True, delme=4)




@app.on_message(gen("pm", allow =["sudo"]))
async def pm_handler(_, m: Message):
	arg = m.command
	if app.long(m) == 1:
		await app.send_edit(m, "Provide me a suffix to do some work.\n\nSuffix: `on` & `off`", delme=4)

	elif app.long(m) > 1 and arg[1] == "on":
		if app.Pmpermit() is True:
			return await app.send_edit(m, "Pmguard is already active !", mono=True, delme=4)

		done = app.setdv("PMPERMIT", "True")
		if done:
			await app.send_edit(m, "Pmguard is now turned on.", mono=True, delme=4)
		else:
			await app.send_edit(m, "Failed to turn on pmguard.", mono=True, delme=4)

	elif app.long(m) > 1 and arg[1] == "off":
		if app.Pmpermit() is False:
			return await app.send_edit(m, "Pmguard is already off !", mono=True, delme=4)

		done = app.deldv("PMPERMIT")
		if done:
			await app.send_edit(m, "Pmguard is now turned off.", mono=True, delme=4)
		else:
			await app.send_edit(m, "Failed to turn off pmguard.", mono=True, delme=4)

	elif app.long(m) > 1 and arg[1] not in ("on", "off"):
		await app.send_edit(m, "Use `on` or `off` after command to turn on & off pmguard.", delme=4)
	else:
		await app.send_edit(m, "Something went wrong, please try again later !", mono=True, delme=4)




@app.on_message(gen("alldv", allow =["sudo"]))
async def alldv_handler(_, m: Message):
	if bool(app.getalldv()) is True:
		m = await app.send_edit(m, "Getting all database vars . . .", mono=True)
		my_dict = app.getalldv()
		dict_data = []
		dict_data.clear()

		for key, value in zip(my_dict.keys(), my_dict.values()):
			dict_data.append(f"`{key}` = `{value}`\n")

		await app.send_edit(m, "**All DB VARS:**\n\n" + "".join(dict_data))
	else:
		await app.send_edit(m, "There are no database vars (empty) !", mono=True, delme=4)



