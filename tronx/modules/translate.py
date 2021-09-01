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
)




CMD_HELP.update(
	{"translate" : (
		"translate",
		{
		"tr [ language code ] [ text ] or [ reply to message ]" : "Translates The Message In Your Language.\n\n**Note :**Use Correct Language Codes To Translate In Your Language."
		}
		)
	}
)




@app.on_message(gen(["tr", "tl"]))
async def translate(_, m: Message):
	replied = m.reply_to_message
	await send_edit(
		m, 
		f"Translating in `{lang}` ..."
		)
	try:
		if len(m.command) > 1:
			lang = m.command[1]
		else:
			lang = "en"
		if (replied 
			and len(m.text) > 1 
			and len(m.text) <= 4096
			and replied.text 
			or replied.caption
			):
			tr = GoogleTranslator(source="auto", target=lang)
			text = replied.text or replied.caption
			output = tr.translate(text)
			await send_edit(
				m, 
				f"**Translated to:** `{lang}`\n\n**Text:** `{output}`"
				)
		elif not replied and len(m.text) <= 4096:
			tr = GoogleTranslator(source="auto", target=lang)
			text = m.text.split(None, 2)[2]
			output = tr.translate(text)
			await send_edit(
				m, 
				f"**Translated to:** `{lang}`\n\n**Text:** `{output}`"
				)
		else:
			await send_edit(
				m, 
				"Invalid language code specified !"
				)
	except Exception as e:
		await error(m, e)



