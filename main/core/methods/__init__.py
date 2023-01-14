from .configs import Configs
from .constants import Constants
from .database import Database
from .decorators import Decorators
from .functions import Functions



class Methods(
    Functions,
    Configs,
    Constants,
    Database,
    Decorators
    ):
    pass