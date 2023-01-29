import inspect

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


class OnUpdate:
    def on_update(
        self,
        handler_type: Union[int, HandlerType],
        filters: pyrogram.filters = None,
        group: int = 0,
        module: str = None,
        usage: str = None
        ):
        """
        parameters::
            handler_type: Union[int, HandleType]
            filters: pyrogram.filters
            group: int

        returns::
            object

        0: CallbackQueryHandler
        1: ChatJoinRequestHandler
        2: ChatMemberUpdatedHandler
        3: ChosenInlineResultHandler
        4: DeletedMessagesHandler
        5: DisconnectHandler
        6: EditedMessageHandler
        7: InlineQueryHandler
        8: MessageHandler
        9: PollHandler
        10: RawUpdateHandler
        11: UserStatusHandler
        """

        if isinstance(handler_type, int):
            handler = handler_type_dict.get(list(handler_type_dict)[handler_type]) 
        else:
            handler = handler_type_dict.get(handler_type)

        if handler is None:
            raise Exception("This handler doesn't exist.")

        if module:
            if not module in self.CMD_HELP.keys():
                self.CMD_HELP.update({module : {}})
            self.CMD_HELP.get(module).update(command_info)
        else:
            # wherever this decorator is called 
            # we will access its future local variables
            frame = inspect.currentframe().f_back
            module = frame.f_locals.get("__name__")

            self.CMD_HELP.get(module.split(".")[-1]).update(command_info)

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    handler(func, filters),
                    group
                )

            return func

        return decorator
