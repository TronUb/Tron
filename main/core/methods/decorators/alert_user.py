import functools
from pyrogram.types import CallbackQuery
from pyrogram.errors import MessageNotModified


# pylint: disable=E1101
class AlertUser:
    def alert_user(self, func):

        @functools.wraps(func)
        async def wrapper(_, cb: CallbackQuery):
            user = cb.from_user

            if not user:
                return  # Ignore callbacks from non-user sources

            if user.id != self.id and user.id not in getattr(self, "SudoUsersList", []):
                await cb.answer(
                    "Sorry, but you can't use this userbot! Make your own userbot at @tronuserbot",
                    show_alert=True,
                )
                return

            try:
                await func(_, cb)
            except MessageNotModified:
                pass  # Ignore this specific error

        return wrapper
