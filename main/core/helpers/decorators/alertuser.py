from pyrogram.types import CallbackQuery
from pyrogram.errors import MessageNotModified





class AlertUser(object):
    def alert_user(self, func):
        async def wrapper(_, cb: CallbackQuery):
            user = cb.from_user
            if user and not (user.id == self.id or user.id in self.SudoUsersList()):
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
