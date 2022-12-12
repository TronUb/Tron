import os

try:
    import uvloop
    uvloop.install()
except ImportError:
    print("uvloop wasn't installed, userbot will work slow.")

from .client import SuperClient


app = SuperClient()
