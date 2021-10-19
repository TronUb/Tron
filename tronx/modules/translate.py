from deep_translator import GoogleTranslator

from pyrogram import filters
from pyrogram.types import Message


from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
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
		"tr [ language code ] [ text ] | [ reply to message ]" : "Translates The Message In Your Language.\n\n**Note :**Use Correct Language Codes To Translate In Your Language."
		}
		)
	}
)




@app.on_message(gen(["tr", "tl"]))
async def translate(_, m: Message):
	reply = m.reply_to_message
	cmd = m.command

	try:
		if long(m) > 1:
			lang = cmd[1]
		else:
			lang = "en"

		if (reply and reply.text):
			text = reply.text
			await translate(m, lang=lang, text=text)

		elif not reply and len(m.text) <= 4096:
			if long(m) <= 2:
				return await send_edit(m, "Give me the language code with text.", mono=True)
			text = m.text.split(None, 2)[2]
			await translate(m, lang=lang, text = text)
			await send_edit(m, f"**Translated to:** `{lang}`\n\n**Text:** `{output}`")
		else:
			await send_edit(m, "Invalid language code specified !", mono=True)
	except Exception as e:
		await error(m, e)




async def translate(m: Message, lang, text):
	await send_edit(m, f"Translating in `{lang}` ...")
	tr = GoogleTranslator(source="auto", target=lang)
	output = tr.translate(text)
	await send_edit(m, f"**Translated to:** `{lang}`\n\n**Text:** `{output}`")




@app.on_message(gen("langs"))
async def supported_language(_, m):
	data = []
	data.clear()

	langs_list = GoogleTranslator.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english:en etc...}
	for x, y in zip(langs_list.values(), langs_list.keys()):
		data.append(f"`{x}` : `{y}`")

	await send_edit(m, "**Total languages:\n\n**" + "\n".join(data))
		
