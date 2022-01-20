



class Initialisation(Collector):
	"""tempclients initialisation"""
	# clients
	tempapp = Client(session_name=Config.SESSION, api_id=Config.API_ID, api_hash=Config.API_HASH)
	tempbot = Client(session_name=Config.SESSION, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.TOKEN)
	# start
	tempapp.start()
	tempbot.start()
	# app
	appdata = tempapp.get_me()
	USER_DC = appdata.dc_id
	USER_ID = appdata.id
	USER_NAME = appdata.first_name
	USER_USERNAME = f"@{appdata.username}" if appdata.username is not None else ""
	# bot
	botdata = tempbot.get_me()
	BOT_DC = botdata.dc_id
	BOT_ID = botdata.id
	BOT_NAME = botdata.first_name
	BOT_USERNAME = f"@{botdata.username}" 
	# stop
	tempapp.stop()
	tempbot.stop()
