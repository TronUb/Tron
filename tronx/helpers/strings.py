from tronx import app




class Strings(object):
	stat_string = f"""
	**Dex:** Stats

	**Location:** /home/stats

	**Name:** {app.REAL_USER_NAME}
	**{app.assistant_name} version:** {app.assistant_version}
	**Python version:** {app.python_version}
	**Pyrogram version:** {app.pyrogram_version}
	**Database:** {app.db_status}
	**Uptime:** {app.uptime()}
	**User Bio:** {app.UserBio}
	"""



	closed_menu_string = f"""
	Welcome to Tron.
	This is your Helpdex, Tap on open button to get more buttons which will help you to understand & operate your userbot & assistant ( LARA )

	• Menu is closed
	"""
