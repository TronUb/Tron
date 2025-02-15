import functools
import inspect
from typing import Callable, Union

import pyrogram
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
        filters: pyrogram.filters = None,
        group: int = 0,
    ) -> Callable:
        """
        Decorator for adding handlers in Pyrogram.

        Parameters:
            handler_type (Union[int, HandlerType]): The handler type (enum or integer index).
            filters (pyrogram.filters, optional): Filters to apply on the handler. Defaults to None.
            group (int, optional): The group number for the handler. Defaults to 0.

        Returns:
            Callable: The decorated function.

        Raises:
            ValueError: If the handler_type is invalid.

        """

        # Convert int to HandlerType if necessary
        if isinstance(handler_type, int):
            try:
                handler_type = list(handler_type_dict.keys())[handler_type]
            except IndexError:
                raise ValueError(f"Invalid handler index: {handler_type}")

        # Get the corresponding handler class
        handler = handler_type_dict.get(handler_type)

        if handler is None:
            raise ValueError(f"Invalid handler type: {handler_type}")

        def decorator(func: Callable) -> Callable:

            @functools.wraps(func)  # Preserve function metadata
            async def wrapper(client: pyrogram.Client, *args, **kwargs):
                return await func(client, *args, **kwargs)

            if isinstance(self, pyrogram.Client):
                self.add_handler(handler(wrapper, filters), group)

            return wrapper

        return decorator
