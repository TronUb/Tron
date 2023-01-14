class Strings(object):
    @property
    def assistant_tab_string(self):
        text = "**Dex:** Assistant\n"
        text += "**Location:**  home/assistant\n\n"
        text += "**Introduction:**\n\n"
        text += "Welcome to assistant tab section."
        text += "There are some buttons below."
        text += "Tap on them to get more details"

        return text


    @property
    def about_tab_string(self):
        text = "**Dex:** About\n"
        text += "**Location:** /home/about\n\n"
        text += "**[ Personal Info ]:**\n\n"
        text += f"**Name:** {self.assistant_name}\n"
        text += "**[ Versions ]:**\n\n"
        text += f"**Python:** {self.python_version}\n"
        text += f"**Pyrogram:** {self.pyrogram_version}\n"
        text += f"**Assistant:**  {self.assistant_version}\n"
        text += "**[ About ]:**\n\n"

        text += "I am Nora made by ࿇•ẞᗴᗩSԵ•࿇.\n"
        text += "I am your friendly assistant,\n"
        text += "I will help you as much as you need.\n"
        text += "You can ask me for any help related to your userbot.\n"
        text += "If you have any suggestions or you're facing any problems\n"
        text += "which are related to tronuserbot then just ask in\n"
        text += f"[support group](https://t.me/TronUbSupport)"

        return text


    @property
    def close_tab_string(self):
        text = "Welcome to Tron.\n"
        text += "This is your Helpdex, Tap on open button to get more buttons,\n"
        text += "which will help you to understand  operate your userbot & assistant ( LARA )\n"
        text += "\n\n• Menu is closed"

        return text


    @property
    def extra_tab_string(self):
        text = "**Dex:** Extra\n\n"
        text += f"Location: /home/extra"

        return text


    @property
    def public_tab_string(self):
        text = "**Dex:** Extra\n"
        text += "**Location:** /home/extra/public commands\n\n"
        text += "**COMMAND:** /start\n**USAGE:** Check that bot is on or off.\n\n"
        text += "**COMMAND:** /help\n**USAGE:** Need help? Type this command.\n\n"
        text += "**COMMAND:** /id\n**USAGE:** Get your id and chat id.\n\n"
        text += "**COMMAND:** /quote\n**USAGE:** Get random anime character quote with a “more” inline button to change random quote infinitely.\n\n"
        text += "**COMMAND:** /ping\n**USAGE:** Test the speed of our bot and get results.\n\n"

        return text


    @property
    def home_tab_string(self):
        text = "**Dex:** Home\n\n"
        text += "**Description:** This is your helpdex use to navigate in different sub dex to information."

        return text


    @property
    def plugin_tab_string(self):
        text = "**Dex:** Plugins \n\n"
        text += "**Location:** /home/plugins\n\n"
        text += f"**Plugins:** `{len(self.CMD_HELP)}`"

        return text


    def restart_tab_string(self, process: str=None):
        text = "**Dex:** Settings\n\n"
        text += "**Location:** /home/settings/restart bot\n"
        text += f"**Process:** {process}"

        return text


    @property
    def settings_tab_string(self):
        text = "**Dex:** Settings\n\n"
        text += "**Location:** /home/settings"

        return text


    def shutdown_tab_string(self, process: str=None):
        text = "**Dex:** Settings\n\n"
        text += "**Location:** /home/settings/shutdown\n"
        text += f"**Process:** {process}"

        return text
 

    @property
    def stats_tab_string(self):
        text = "**Dex:** Stats\n"
        text += "**Location:** /home/stats\n\n"
        text += f"**Name:** {self.UserName}\n"
        text += f"**{self.BotName} version:** {self.assistant_version}\n"
        text += f"**Python version:** {self.python_version}\n"
        text += f"**Pyrogram version:** {self.pyrogram_version}\n"
        text += f"**Database:** {self.db_status()}\n"
        text += f"**Uptime:** {self.uptime()}\n"
        text += f"**User Bio:** {self.UserBio}\n"

        return text


    @property
    def update_tab_string(self):
        text = "Not implemented yet."

        return text


    @property
    def ialive_tab_string(self):
        text = f"**⛊  Inline Status:**\n\n"
        text += f"**⟐** {self.UserBio}\n\n"
        text += f"**⟜ Owner**: [{self.name}](https://t.me/{self.username})\n"
        text += f"**⟜ Tron:** `{self.userbot_version}`\n"
        text += f"**⟜ Python:** `{self.python_version}`\n"
        text += f"**⟜ Pyrogram:** `{self.pyrogram_version}`\n"
        text += f"**⟜ uptime:** `{self.uptime()}`\n"

        return text



    @property
    def pmpermit_tab_string(self):
        text = "Not implemented yet."

        return text


