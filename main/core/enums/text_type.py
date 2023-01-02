from enum import auto

from .auto_name import AutoName


class TextType(AutoName):

    DEFAULT = auto()

    MONO = auto()

    ITALIC = auto()

    BOLD = auto()