import os

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import BotInlineDisabled

from tronx import app

from pyrogram.types import (
	Message,
	CallbackQuery,
)

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"help" : (
		"help",
		{
		"help [ module name ]" : "Get commands info of that plugin.",
		"help" : "Get your inline help dex.",
		"inline" : "Toggle inline mode to On or Off of your bot through @BotFather",
		"mods" : "Get list of available module names",
		"plugs" : "Get list of available plugin names",
		}
		)
	}
)


helpdex_ids = [x for x in app.getdv("DELETE_DEX_ID").strip("[]").split("," " ") if bool(app.getdv("DELETE_DEX_ID"))]


@app.bot.on_callback_query(filters.regex("delete-dex"))
@app.alert_user
async def delete_helpdex(_, cb: CallbackQuery):
	if not bool(helpdex_ids):
		await cb.answer(
			"This message is expired, hence it can't be deleted !",
			show_alert=True,
		)
	else:
		try:
			for x in helpdex_ids: # list
				for y in x: # dicts
					done = await app.delete_messages(int(y), x[y])
					if not done:
						await cb.answer(
							"This message is expired, hence it can't be deleted !",
							show_alert=True,
						)
		except Exception as e:
			app.log.error(e)





@app.on_message(gen("help", allow =["sudo"]))
async def help_menu(_, m: Message):
	args = m.command if app.long(m) > 1 else False

	try:
		if args is False:
			m = await app.send_edit(m, ". . .", mono=True)
			result = await app.get_inline_bot_results(
				app.bot.username, 
				"#t5r4o9nn6" 
			)
			if result:
				await m.delete()
				info = await app.send_inline_bot_result(
					m.chat.id, 
					query_id=result.query_id, 
					result_id=result.results[0].id, 
					disable_notification=True, 
					hide_via=True
				)
				
				if m.chat.type in ["bot", "private"]:
					app.setdv("DELETE_DEX_ID", helpdex_ids.append({m.chat.id : info.updates[1].message.id}))
				else:
					app.setdv("DELETE_DEX_ID", helpdex_ids.append({m.chat.id : info.updates[2].message.id}))
			else:
				await app.send_edit(m, "Please check your bots inline mode is on or not . . .", delme=3, mono=True)
		elif args:

			module_help = await app.data(args[1])
			if not module_help:
				await app.send_edit(m, f"Invalid module name specified, use `{app.PREFIX}mods` to get list of modules", delme=3)
			else:
				await app.send_edit(m, f"**MODULE:** {args[1]}\n\n" + "".join(module_help))
		else:
			await app.send_edit(m, "Try again later !", mono=True, delme=3)
	except BotInlineDisabled:
		await app.toggle_inline(m)
		await help_menu(client, m)
	except Exception as e:
		await app.error(m, e)




# get all module name
@app.on_message(gen("mods", allow =["sudo"]))
async def all_modules(_, m: Message):
	store = []
	for x in os.listdir("tronx/modules/"):
		if not x in ["__pycache__", "__init__.py"]:
			store.append(x + "\n")

	await app.send_edit(m, "Modules of userbot:\n\n" + "".join(store))




# get all plugins name
@app.on_message(gen("plugs", allow =["sudo"]))
async def all_plugins(_, m: Message):
	store = []
	for x in os.listdir("tronx/plugins/"):
		if not x in ["__pycache__", "__init__.py"]:
			store.append(x + "\n")

	await app.send_edit(m, "Plugins of bot:\n\n" + "".join(store))




@app.on_message(gen("inline", allow =["sudo"]))
async def _toggle_inline(_, m: Message):
	return await app.toggle_inline(m)


