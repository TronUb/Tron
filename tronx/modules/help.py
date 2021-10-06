from pyrogram import filters

from tronx import (
	app, 
	CMD_HELP, 
	HELP, 
	Config,
	PREFIX
	)

from pyrogram.types import Message

from tronx.helpers import (
	error,
	gen,
	send_edit,
	BOT_USERNAME,
	# others 
	get_arg,
	delete,
)




plugin_data = []


CMD_HELP.update(
	{"help" : (
		"help",
		{
		"help [ module name ]" : "Get commands info of that plugin.",
		"help" : "Get your inline help dex.",
		}
		)
	}
)




@app.on_message(gen("help"))
async def help_menu(app, m):
	args = get_arg(m)
	try:
		if not args:
			await send_edit(m, "`...`")
			result = await app.get_inline_bot_results(
				BOT_USERNAME, 
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
				await send_edit(m, "Please check your bots inline mode is on or not . . .", delme=3)
			return
		elif args:
			plugin_data.clear()
			module_help = await data(args)
			if not module_help:
				await send_edit(m, f"Invalid module name specified, use `{PREFIX}cmds` to get list of plugins.", delme=3)
				return
			else:
				await send_edit(m, f"PLUGIN: {args}\n\n" + "".join(plugin_data))
		else:
			await send_edit(m, "Failed to get help menu !", delme=3)
	except Exception as e:
		await error(m, e)




# get all plugins name
@app.on_message(gen("plugs"))
async def all_plugins(_, m: Message):
	await send_edit(
		m, 
		"\n".join(CMD_HELP.keys())
		)




async def data(plug):
	try:
		for x, y in zip(
			CMD_HELP.get(plug)[1].keys(), 
			CMD_HELP.get(plug)[1].values()
			):
			plugin_data.append(
				f"CMD: `{PREFIX}{x}`\nINFO: `{y}`\n\n"
				)
		return True
	except Exception as e:
		print(e)
		return False


