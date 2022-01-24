from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tronx import app





@app.bot.on_message(filters.command("id"))
async def id_of_user(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.bot.send_message(
			m.chat.id,
			f"**YOUR ID:** `{m.from_user.id}`\n**CHAT ID:** `{m.chat.id}`"
		)
	elif reply:
		await app.bot.send_message(
			m.chat.id,
			f"**REPLIED USER ID:** `{m.from_user.id}`\n**CHAT ID:** `{m.chat.id}`\n**REPLIED ID:** `{reply.from_user.id}`"
		)




@app.bot.on_message(filters.command("quote"))
async def get_anime_quotes(_, m):
	await app.bot.send_message(
		m.chat.id,
		app.quote(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"More", callback_data="more-anime-quotes"
					)
				],
			]
		)
	)


