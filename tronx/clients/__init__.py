import uvloop
from .client import SuperClient



# performance boost
uvloop.install()

app = SuperClient()
