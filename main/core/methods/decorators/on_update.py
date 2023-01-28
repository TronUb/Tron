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
    UserStatusHandler
)

from typing import Callable, Union

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
    HandlerType.USER_STATUS: UserStatusHandler
}


def generate_docs():
    return [
        f"{x} : {handler_type_dict.get(list(handler_type_dict)[x])}\n" for 
        x in range(len(handler_type_dict))
    ]


class OnUpdate:
    """
    parameters::
        handler_type: Union[int, HandleType]
        filters: pyrogram.filters
        group: int
    
    Note:
        {}
    """.format(*generate_docs())
    def on_update(
        self,
        handler_type: Union[int, HandlerType],
        filters: pyrogram.filters = None,
        group: int = None
        ):
        if isinstance(handler_type, int):
            handler = handler_type_dict.get(list(handler_type_dict)[handler]) 
        else:
            handler = handler_type_dict.get(handler_type)

        if handler is None:
            raise Exception("This handler doesn't exist.")

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    handler(func, filters),
                    group
                )

            return func

        return decorator
