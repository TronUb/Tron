import functools
import inspect
from typing import Callable, Union, Optional

import pyrogram
from pyrogram.filters import Filter
from pyrogram.handlers import (
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ChatMemberUpdatedHandler,
    ChosenInlineResultHandler,
    DeletedMessagesHandler,
    DisconnectHandler,
    EditedMessageHandler,
    InlineQueryHandler,
    MessageHandler,
    PollHandler,
    RawUpdateHandler,
    UserStatusHandler,
)

from main.core.enums import HandlerType


# Mapping of HandlerType enums to actual Pyrogram handler classes
handler_type_dict = {
    HandlerType.CALLBACK_QUERY: CallbackQueryHandler,
    HandlerType.CHAT_JOIN_REQUEST: ChatJoinRequestHandler,
    HandlerType.CHAT_MEMBER_UPDATED: ChatMemberUpdatedHandler,
    HandlerType.CHOSEN_INLINE_RESULTS: ChosenInlineResultHandler,
    HandlerType.DELETED_MESSAGES: DeletedMessagesHandler,
    HandlerType.DISCONNECT: DisconnectHandler,
    HandlerType.EDITED_MESSAGE: EditedMessageHandler,
    HandlerType.INLINE_QUERY: InlineQueryHandler,
    HandlerType.MESSAGE: MessageHandler,
    HandlerType.POLL: PollHandler,
    HandlerType.RAW_UPDATE: RawUpdateHandler,
    HandlerType.USER_STATUS: UserStatusHandler,
}


class OnUpdate:
    def on_update(
        self,
        handler_type: Union[int, HandlerType],
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:
        """
        Decorator for registering update handlers in Pyrogram via a unified interface.

        Args:
            handler_type (int | HandlerType): Handler type enum or index.
            filters (pyrogram.filters.Filter, optional): Filter for the handler.
            group (int, optional): Handler execution group.

        Returns:
            Callable: A decorator for the async function that handles the update.
        """

        # Allow passing handler index directly
        if isinstance(handler_type, int):
            try:
                handler_type = list(handler_type_dict.keys())[handler_type]
            except IndexError:
                raise ValueError(f"Invalid handler index: {handler_type}")

        handler_class = handler_type_dict.get(handler_type)
        if not handler_class:
            raise ValueError(f"Invalid handler type: {handler_type}")

        def decorator(func: Callable) -> Callable:

            @functools.wraps(func)
            async def wrapper(client: pyrogram.Client, *args, **kwargs):
                return await func(client, *args, **kwargs)

            if isinstance(self, pyrogram.Client):
                self.add_handler(handler_class(wrapper, filters), group)
            else:
                raise TypeError(
                    "Decorator can only be used within a pyrogram.Client instance."
                )

            return wrapper

        return decorator
