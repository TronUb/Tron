from .botconfig import BotConfig, BOTDV
from .otherconfig import OtherConfig, OTHERDV
from .userconfig import UserConfig, USERDV




class DataVars(
	BotConfig,
	OtherConfig,
	UserConfig
	):
	DVLIST = BOTDV + OTHERDV + USERDV
