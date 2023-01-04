from enum import auto

from .auto_name import AutoName


class ReplyType(AutoName):

    TEXT = auto()
    
    PHOTO = auto()
    
    AUDIO = auto()
    
    ANIMATION = auto()
    
    DOCUMENT = auto()
    
    STICKER = auto()
