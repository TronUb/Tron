from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton

from tronx import (
	bot
)

from tronx.helpers import (
	error,
	quote,
)




@bot.on_message(filters.command("id"))
async def id_of_user(_, m):
	reply = m.reply_to_message
	if not reply:
		await bot.send_message(
			m.chat.id,
			f"**YOUR ID:** `{m.from_user.id}`\n**CHAT ID:** `{m.chat.id}`"
		)
	elif reply:
		await bot.send_message(
			m.chat.id,
			f"**YOUR ID:** `{m.from_user.id}`\n**CHAT ID:** `{m.chat.id}`\n**REPLIED ID:** `{reply.from_user.id}`"
		)




@bot.on_message(filters.command("quote"))
async def get_anime_quotes(_, m):
	await bot.send_message(
		m.chat.id,
		quote(),
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


