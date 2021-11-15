from pyrogram import filters

from tronx import (
	app, 
	CMD_HELP, 
	HELP, 
	Config,
	PREFIX, 
	)

from pyrogram.types import Message

from tronx.helpers import (
	error,
	gen,
	send_edit,
	# others
	delete,
	botusername,
	data,
	toggle_inline,
)




CMD_HELP.update(
	{"help" : (
		"help",
		{
		"help [ module name ]" : "Get commands info of that plugin.",
		"help" : "Get your inline help dex.",
		"inline" : "Toggle inline mode to On or Off of your bot through @BotFather",
		}
		)
	}
)




@app.on_message(gen("help"))
async def help_menu(app, m):
	cmd = m.command
	if len(cmd) > 1:
		args = cmd[1]
	else:
		args = False
	try:
		if args is False:
			await send_edit(m, "...", mono=True)
			result = await app.get_inline_bot_results(
				botusername(), 
				"#t5r4o9nn6" 
			)
			if result:
				await m.delete()
				await app.send_inline_bot_result(
					m.chat.id, 
					query_id=result.query_id, 
					result_id=result.results[0].id, 
					disable_notification=True, 
					hide_via=True
				)
			else:
				await send_edit(m, "Please check your bots inline mode is on or not . . .", delme=3, mono=True)
		elif args:
			plugin_data = []
			plugin_data.clear()

			module_help = await data(args[1])
			if not module_help:
				await send_edit(m, f"Invalid module name specified, use `{PREFIX}mods` to get list of modules", delme=3)
			else:
				await send_edit(m, f"**MODULE:** {args[1]}\n\n" + "".join(plugin_data))
		else:
			await send_edit(m, "Failed to get help menu !", delme=3)
	except Exception as e:
		await error(m, e)




# get all plugins name
@app.on_message(gen("mods"))
async def all_plugins(_, m: Message):
	store = []
	for x in os.listdir("tronx/modules/"):
		if not x in ["__pycache__", "__init__.py"]:
			store.append(x + "\n")

	await send_edit(
		m,
		"Modules of userbot:\n\n" + "".join(store)
		)




@app.on_message(gen("plugs"))
async def all_plugins(_, m: Message):
	store = []
	for x in os.listdir("tronx/plugins/"):
		if not x in ["__pycache__", "__init__.py"]:
			store.append(x + "\n")

	await send_edit(
		m,
		"Modules of userbot:\n\n" + "".join(store)
		)




@app.on_message(gen("inline"))
async def _toggle_inline(_, m: Message):
	await send_edit(m, "Processing command . . .", mono=True)
	await toggle_inline(m)
	return






#async def data(plug):
#	try:
#		for x, y in zip(
#			CMD_HELP.get(plug)[1].keys(), 
#			CMD_HELP.get(plug)[1].values()
#			):
#			plugin_data.append(
#				f"CMD: `{PREFIX}{x}`\nINFO: `{y}`\n\n"
#				)
#		return True
#	except Exception as e:
#		print(e)
#		return False


