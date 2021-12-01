import os

from pyrogram import filters

from tronx import (
	app, 
	bot, 
	CMD_HELP, 
	HELP, 
	Config,
	PREFIX, 
	USER_ID,
	)

from pyrogram.types import (
	Message,
	CallbackQuery,
)

from tronx.helpers import (
	error,
	gen,
	send_edit,
	# others
	delete,
	botusername,
	data,
	toggle_inline,
	long,
	message_ids,
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





@bot.on_callback_query(filters.regex("delete-dex") & filters.user(USER_ID))
async def delete_helpdex(_, cb: CallbackQuery):
	if bool(message_ids) is False:
		await cb.answer(
			"This message is expired, hence it can't be deleted !",
			show_alert=True,
		)
	else:
		try:
			for chat_id, msg_id in zip(list(message_ids.keys()), list(message_ids.values())):
				done = await app.delete_messages(chat_id, msg_id)
				if done is False:
					await cb.answer(
						"This message is expired, hence it can't be deleted !",
						show_alert=True,
					)
		except Exception as e:
			print(e)





@app.on_message(gen("help"))
async def help_menu(app, m):
	args = m.command if long(m) > 1 else False

	try:
		if args is False:
			await send_edit(m, ". . .", mono=True)
			result = await app.get_inline_bot_results(
				botusername(), 
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
					message_ids.update({m.chat.id : info.updates[1].message.id})
				else:
					message_ids.update({m.chat.id : info.updates[2].message.id})
			else:
				await send_edit(m, "Please check your bots inline mode is on or not . . .", delme=3, mono=True)
		elif args:

			module_help = await data(args[1])
			if not module_help:
				await send_edit(m, f"Invalid module name specified, use `{PREFIX}mods` to get list of modules", delme=3)
			else:
				await send_edit(m, f"**MODULE:** {args[1]}\n\n" + "".join(module_help))
		else:
			await send_edit(m, "Try again later !", mono=True, delme=3)
	except Exception as e:
		await error(m, e)




# get all module name
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




# get all plugins name
@app.on_message(gen("plugs"))
async def all_plugins(_, m: Message):
	store = []
	for x in os.listdir("tronx/plugins/"):
		if not x in ["__pycache__", "__init__.py"]:
			store.append(x + "\n")

	await send_edit(
		m,
		"Plugins of bot:\n\n" + "".join(store)
		)




@app.on_message(gen("inline"))
async def _toggle_inline(_, m: Message):
	await toggle_inline(m)
	return

