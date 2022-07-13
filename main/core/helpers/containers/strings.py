class Strings(object):
	def stats_tab_string(self):
		text = "**Dex:** Stats\n"
		text += "**Location:** /home/stats\n\n"
		text += f"**Name:** {self.UserName()}\n"
		text += f"**{self.BotName()} version:** {self.assistant_version}\n"
		text += f"**Python version:** {self.python_version}\n"
		text += f"**Pyrogram version:** {self.pyrogram_version}\n"
		text += f"**Database:** {self.db_status()}\n"
		text += f"**Uptime:** {self.uptime()}\n"
		text += **User Bio:** {self.UserBio()}\n"

		return text


	def closed_tab_string(self):
		text = "Welcome to Tron.\n"
		text += "This is your Helpdex, Tap on open button to get more buttons,\n"
		text += "which will help you to understand  operate your userbot & assistant ( LARA )\n"
		text += "\n\n• Menu is closed"

		return text


	def about_tab_string(self):
		text = "**Dex:** About\n"
		text += "**Location:** /home/about\n"
		text += "**[ Personal Info ]:**\n\n"
		text += f"**Name:** {app.assistant_name}\n"
		text += "**[ Versions ]:**\n\n"
		text += f"**Python:** {app.python_version}\n"
		text += f"**Pyrogram:** {app.pyrogram_version}\n"
		text += f"**Assistant:**  {app.assistant_version}\n"
		text += "**[ About ]:**\n\n"

		text += "I am Nora made by ࿇•ẞᗴᗩSԵ•࿇.\n"
		text += "I am your friendly assistant,\n"
		text += "I will help you as much as you need.\n"
		text += "You can ask me for any help related to your userbot.\n"
		text += "If you have any suggestions or you're facing any problems\n"
		text += "which are related to tronuserbot then just ask in\n"
		text += f"[support group](https://t.me/tronuserbot_support)"

		return text


	def extra_tab_string(self):
		text = "**Dex:** Extra\n\n"
		text += f"Location: /home/extra"

		return text


	def public_tab_string(self):
		text = "**Dex:** Extra\n"
		text += "**Location:** /home/extra/public commands\n\n"
		text += "**COMMAND:** /start\n**USAGE:** Check that bot is on or off.\n\n"
		text += "**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n"
		text += "**COMMAND:** /id\n**USAGE:** Get your id and chat id.\n\n"
		text += "**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n"
		text += "**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n"

		return text


	def home_tab_string(self):
		text = "**Dex:** Home\n\n"
		text += "**Description:** This is your helpdex use to navigate in different sub dex to information."

		return text













