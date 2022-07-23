import uvloop
from .client import SuperClient


uvloop.install()
app = SuperClient()
