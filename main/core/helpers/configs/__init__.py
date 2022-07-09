from .botconfig import BotConfig, BOTDV
from .otherconfig import OtherConfig, OTHERDV
from .userconfig import UserConfig, USERDV
from .pmpermitconfig import PmpermitConfig, PMPERMITDV
from .afkconfig import AfkConfig, AFKDV




class Configs(
	BotConfig,
	OtherConfig,
	PmpermitConfig,
	UserConfig,
	AfkConfig
	):
	DVLIST = BOTDV + OTHERDV + USERDV + PMPERMITDV + AFKDV   
