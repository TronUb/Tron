from pyrogram.types import (
	InlineKeyboardMarkup, 
	InlineKeyboardButton,
)

from tronx import app

from tronx.helpers import (
	gen,
)




@app.on_message(gen("kbd", allow = ["sudo"]))
async def create_keyboard(_, m):
	await m.delete()
	if m.chat.type == "bot":
		return await app.send_edit(m, "Sorry you can't use it here", mono=True)
	if app.long(m) >= 3:
		await app.bot.send_message(
			m.chat.id, 
			m.text.split(None, 3)[3],
				reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton( 
						m.command[1],
						url=m.command[2]
					),
					],
				]
				)
			)
	else:
		await app.send_edit(m, f"`{app.PREFIX}kbd [ Button text ] [ Button url ] [ Text ]`")
