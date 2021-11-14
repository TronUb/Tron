from deep_translator import GoogleTranslator

from pyrogram.types import Message


from tronx import (
	app, 
	CMD_HELP,
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	long,
)




CMD_HELP.update(
	{"translate" : (
		"translate",
		{
		"tr [ language code ] [ text ] | [ reply to message ]" : "Translates The Message In Your Language.\n\n**Note :**Use Correct Language Codes To Translate In Your Language.",
		"langs" : "Get list of supported translating languages."
		}
		)
	}
)




@app.on_message(gen(["tr", "tl"]))
async def translate(_, m: Message):
	reply = m.reply_to_message
	cmd = m.command

	try:
		lang = cmd[1] if long(m) > 1 else "en"

		await send_edit(m, f"**Translating in** `{lang}` . . .")

		languages = list((GoogleTranslator.get_supported_languages(as_dict=True)).values())

		if not lang in languages:
			return await send_edit(m, "Bot doesn't support this language code, please try different one.", mono=True, delme=5)

		if (reply and reply.text):
			tdata = await translate(m, lang=lang, text=reply.text)
			await send_edit(m, f"**Translated to:** `{lang}`\n\n**Text:**`{tdata}`")

		elif not reply and len(m.text) <= 4096:
			if long(m) <= 2:
				return await send_edit(m, "Give me the language code with text.", mono=True, delme=3)
			text = m.text.split(None, 2)[2]
			tdata = await translate(m, lang=lang, text=text)
			await send_edit(m, f"**Translated to:** `{lang}`\n\n**Text:** `{tdata}`")
		else:
			await send_edit(m, "Something went wrong, please try again later !", mono=True, delme=5)
	except Exception as e:
		await error(m, e)




async def translate(m: Message, lang, text):
	tr = GoogleTranslator(source="auto", target=lang)
	output = tr.translate(text)
	return output




@app.on_message(gen("langs"))
async def supported_language(_, m):
	data = []
	data.clear()

	langs_list = GoogleTranslator.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english: en etc...}
	for x, y in zip(langs_list.values(), langs_list.keys()):
		data.append(f"`{x}` : `{y}`")

	await send_edit(m, "**Total languages:**\n\n" + "\n".join(data))
		
