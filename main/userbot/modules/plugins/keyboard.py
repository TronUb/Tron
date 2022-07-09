from pyrogram.types import (
	InlineKeyboardMarkup, 
	InlineKeyboardButton,
)

from main import app, gen




@app.on_message(gen("kbd", allow = ["sudo"]))
async def create_keyboard(_, m):
	await m.delete()
	if m.chat.type == "bot":
		return await app.send_edit("Sorry you can't use it here", delme=3, text_type=["mono"])

	if not await app.user_exists(app.bot.id, m.chat.id):
		return await app.send_edit("Your bot is not present in this group.", text_type=["mono"], delme=4)

	if app.long() >= 3:
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
		await app.send_edit(f"`{app.Trigger()[0]}kbd [ Button text ] [ Button url ] [ Text ]`")
