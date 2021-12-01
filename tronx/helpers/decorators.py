from pyrogram.types import CallbackQuery
from .variables import USER_ID
from pyrogram.errors import MessageNotModified






def alert_user(func):
	async def wrapper(_, cb: CallbackQuery):
		if cb.from_user and not cb.from_user.id in USER_ID:
			await cb.answer(
				f"Sorry, but you can't use this userbot ! make your own userbot at @tronuserbot", 
				show_alert=True
			)
		else:
			try:
				await func(_, cb)
			except MessageNotModified:
				pass
	return wrapper
