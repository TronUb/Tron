from .botconfig import BotConfig, BOTDV
from .otherconfig import OtherConfig, OTHERDV
from .userconfig import UserConfig, USERDV
from .pmpermitconfig import PmpermitConfig, PMPERMITDV
from .afkconfig import AfkConfig, AFKDV
from .herokuconfig import HerokuConfig, HEROKUDV




class Configs(
    BotConfig,
    OtherConfig,
    PmpermitConfig,
    UserConfig,
    AfkConfig,
    HerokuConfig
    ):
    DVLIST = BOTDV + OTHERDV + USERDV + PMPERMITDV + AFKDV + HEROKUDV  
