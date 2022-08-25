try:
    import uvloop
except ImportError:
    uvloop = None

from .client import SuperClient



# support for termux
if uvloop:
    uvloop.install()

# create an instance of client
app = SuperClient()
