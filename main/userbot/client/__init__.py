import os
from main.colors import Colors


try:
    import uvloop
    uvloop.install()
except ImportError:
    print(Colors.block + Colors.red + "\nuvloop wasn't installed, userbot will work slow.\n" + Colors.reset)

from .client import SuperClient


app = SuperClient()
