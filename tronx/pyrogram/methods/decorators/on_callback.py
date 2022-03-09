from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.scaffold import Scaffold


class OnCallbackQuery(Scaffold):
    def on_callback(
        self=None,
        filters=None,
        group: int = 0
    ) -> callable:

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.CallbackQueryHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.CallbackQueryHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator

