import os
from main.colors import Colors


try:
    import uvloop
    uvloop.install()
except ImportError:
    print(Colors.block + Colors.red + Colors.white + "uvloop wasn't installed, userbot will work slow." + Colors.reset)

from .client import SuperClient


app = SuperClient()
