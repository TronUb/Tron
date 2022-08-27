import os

try:
    # work slow but don't mess
    print("uvloop wasn't installed, userbot will work slow.")
    import uvloop
except ImportError:
    pass

from .client import SuperClient



if uvloop:
    uvloop.install()

app = SuperClient()
