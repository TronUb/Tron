from enum import auto

from .auto_name import AutoName


class HandlerType(AutoName):

    CALLBACK_QUERY = auto()

    CHAT_JOIN_REQUEST = auto()

    CHAT_MEMBER_UPDATED = auto()

    CHOSEN_INLINE_RESULTS = auto()

    DELETED_MESSAGES = auto()

    DISCONNECT = auto()

    EDITED_MESSAGE = auto()

    INLINE_QUERY = auto()

    MESSAGE = auto()

    POLL = auto()

    RAW_UPDATE = auto()

    USER_STATUS = auto()
