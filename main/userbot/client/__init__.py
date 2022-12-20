import os
from main.colors import Colors


try:
    import uvloop
    uvloop.install()
except ImportError:
    print(Colors.block + Colors.red + "uvloop wasn't installed, userbot will work slow." + Colors.reset)

from .client import SuperClient


app = SuperClient()
