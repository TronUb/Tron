from enum import auto

from .auto_name import AutoName


class SudoType(AutoName):

    DEV = auto()
    
    COMMON = auto()
    
    UNKNOWN = auto()