from .botconfig import BotConfig, BOTDV
from .otherconfig import OtherConfig, OTHERDV
from .userconfig import UserConfig, USERDV
from .pmpermitconfig import PmpermitConfig, PMPERMITDV




class Configs(
	BotConfig,
	OtherConfig,
	PmpermitConfig,
	UserConfig
	):
	DVLIST = BOTDV + OTHERDV + USERDV + PMPERMITDV
