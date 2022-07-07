from main.assistant.client import bot

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton





@bot.on_message(filters.command("id"), group=-1)
async def chat_user_id(_, m):
	reply = m.reply_to_message
	if not reply:
		await bot.send_message(
			m.chat.id,
			f"**{m.from_user.first_name}:** `{m.from_user.id}`\n**{m.chat.title}:** `{m.chat.id}`"
		)
	elif reply:
		await bot.send_message(
			m.chat.id,
			f"**{m.from_user.first_name}:** `{m.from_user.id}`\n**{m.chat.title}:** `{m.chat.id}`\n**{reply.from_user.first_name}:** `{reply.from_user.id}`"
		)




@bot.on_message(filters.command("quote"), group=-1)
async def bot_anime_quotes(_, m):
	await bot.send_message(
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


