import time

from tronx.database.postgres import dv_sql as db

from pyrogram.types import Message

from tronx import (
	app,
)

from tronx.helpers import (
	gen,
	long,
	send_edit,
	error,
)




@app.on_message(gen("setdv"))
async def set_dv_var(_, m: Message):
	if long(m) == 2:
		await send_edit(m, "Please give me key with a value . . . ")  
		return
	if long(m) > 2 and long(m) < 4096:
		key = m.command[1]
		value = m.text.split(None, 2)[2]
		done = db.setdv(key, value)
		if done:
			await send_edit(
				m, 
				f"Added database var with key = `{key}` and value = `{value}`"
				)   
		elif not done:
			await send_edit(
				m, 
				"Failed to a add key & value to database var . . ."
				)
	else:
		await send_edit(
			m, 
			"Maximum 4096 characters in one message . . ."
			)




@app.on_message(gen("deldv"))
async def del_dv_var(_, m: Message):
	if long(m) == 1:
		await send_edit(
			m, 
			"Give me some key to delete that a var from database . . . "
		)  
	elif long(m) > 1:
		key = m.command[1]
		done = db.deldv(key)
		await send_edit(
			m, 
			f"Successfully deleted key = `{key}`"
		)   
	else:
		await send_edit(
			m, 
			"Maximum 4096 characters in one message . . ."
			)




@app.on_message(gen("getdv"))
async def get_dv_var(_, m: Message):
	if long(m) == 1:
		await send_edit(
			m, 
			"Give me some key to get value that a var from database . . . "
		)  
	elif long(m) > 1:
		key = m.command[1]
		done = db.getdv(key)
		if done:
			await send_edit(
				m, 
				f"Here:\n\nkey = `{key}`\n\nvalue = `{done}`"
				)   
		elif not done:
			await send_edit(
				m, 
				"This var doesn't exist in my database . . ."
				)
	else:
		await send_edit(
			m, 
			"Maximum 4096 characters in one message . . ."
			)