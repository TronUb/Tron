from enum import auto

from .auto_name import AutoName


class UserType(AutoName):

    OWNER = auto()

    SUDO = auto()

    OTHER = auto()

    ALL = auto()