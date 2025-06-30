# pylint: disable=E1101

import functools
from typing import Callable, Awaitable, Any

from pyrogram.types import CallbackQuery
from pyrogram.errors import MessageNotModified


class AlertUser:
    """
    Decorator class to restrict callback query interactions
    to the userbot owner or authorized sudo users.
    """

    def alert_user(
        self, func: Callable[..., Awaitable[Any]]
    ) -> Callable[..., Awaitable[None]]:

        @functools.wraps(func)
        async def wrapper(_, cb: CallbackQuery):
            user = cb.from_user

            if not user:
                return  # Ignore anonymous callbacks

            # Sudo access check
            sudo_list = getattr(self, "SudoUsersList", [])
            if user.id != self.id and user.id not in sudo_list:
                await cb.answer(
                    "🚫 You're not allowed to use this userbot.\nBuild your own from @tronuserbot.",
                    show_alert=True,
                )
                return

            try:
                await func(_, cb)
            except MessageNotModified:
                pass  # Silently ignore this specific benign error

        return wrapper
