from .client import SuperClient
import uvloop


uvloop.install()

app = SuperClient()
