from tronx import (
	USER_NAME, 
	python_version, 
	pyrogram_version, 
	assistant_version,
	db_status, 
	uptime, 
	USER_BIO,
)

from .variables import (
	assistant_name
)




stat_string = f"""
**Dex:** Stats

**Location:** /home/stats

**Name:** {USER_NAME}
**{assistant_name} version:** {assistant_version}
**Python version:** {python_version}
**Pyrogram version:** {pyrogram_version}
**Database:** {db_status}
**Uptime:** {uptime()}
**User Bio:** {USER_BIO}
"""



closed_menu_string = f"""
Welcome to Tron.
This is your Helpdex, Tap on open button to get more buttons which will help you to understand & operate your userbot & assistant ( LARA )

• Menu is closed
"""
