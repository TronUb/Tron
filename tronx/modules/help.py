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
	data,
)




plugin_data = []


CMD_HELP.update(
	{ 
		"help": f"""
**PLUGIN:** `help`\n\n
**COMMAND:** {PREFIX}help [ module name ] \n**USAGE:** Get commands info of that plugin.\n
**COMMAND:** {PREFIX}help \n**USAGE:** get your inline help dex.\n
"""
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
				await send_edit(
					m, 
					"Please check your bots inline mode is on or not ..."
					)
			return
		elif args:
			plugin_data.clear()
			module_help = await data(args)
			if not module_help:
				await send_edit(
					m, 
					f"Invalid module name specified, use `{PREFIX}cmds` to get list of plugins."
				)
				await delete(m, 2)
				return
			else:
				await send_edit(
					m, 
					f"{args}\n\n" + "".join(plugin_data)
					)
		else:
			await send_edit(
				m, 
				"Failed to get help menu !"
				)
	except Exception as e:
		await error(m, e)




# get all plugins name
@app.on_message(gen("cmds"))
async def all_plugins(_, m: Message):
	plugs = list(CMD_HELP.keys())
	await send_edit(
		m, 
		"\n".join(plugs)
		)

