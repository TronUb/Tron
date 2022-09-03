import os

try:
    import uvloop
except ImportError:
    print("uvloop wasn't installed, userbot will work slow.")

from .client import SuperClient



if uvloop:
    uvloop.install()

app = SuperClient()
