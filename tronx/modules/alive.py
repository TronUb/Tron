from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
	)

from tronx.helpers import (
	gen,
	alive,
	ialive,
	quote,
)




CMD_HELP.update(
	{
		"alive":f"""
**PLUGIN:** `alive`\n\n
**COMMAND:** `{PREFIX}alive` \n**USAGE:** Normal alive, in which you will get userbot status without inline buttons.\n\n
**COMMAND:** `{PREFIX}ialive` \n**USAGE:** Inline alive that contains your & your userbot status.\n\n
"""
	}
)




# commands
@app.on_message(gen("alive"))
async def alive(app, m: Message):
	await alive(m)




@app.on_message(gen(["ialive", "inline"]))
async def inline_alive(app, m: Message):
	await ialive(m)




@app.on_message(gen(["qt"]))
async def inline_alive(app, m):
	await quote(m)




