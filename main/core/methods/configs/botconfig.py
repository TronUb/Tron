""" bot configuration module """

BOTDV = [
    "BOT_NAME",
    "BOT_USERNAME",
    "BOT_ID",
    "BOT_BIO",
    "BOT_PIC"
    ]


class BotConfig(object):
    """ bot configuration module """
    @property
    def BotName(self):
        """Get your bot name"""
        return self.getdv("BOT_NAME") or self.BOT_NAME or self.bot.name or None


    @property
    def BotUserName(self):
        """Get your bot username"""
        return self.getdv("BOT_USERNAME") or self.BOT_USERNAME or self.bot.username or None


    @property
    def BotMention(self):
        """Get bot mention"""
        return f"[{self.BotName}](tg://user?id={self.BotId})" if self.BotName and self.BotId else None


    @property
    def BotId(self):
        """Get your bots telegram id"""
        return self.getdv("BOT_ID") or self.BOT_ID or self.bot.id or None


    def BotBio(self, m):
        """Get your bots bio"""
        official = f"Hey {m.from_user.mention} my name is {self.BotName} and I am your assistant bot. I can help you in many ways . Just use the buttons below to get list of possible commands."
        get_bio = self.getdv("BOT_BIO") or self.BOT_BIO or official or ""
        return f"{get_bio}\n\n**Catagory: **"


    @property
    def BotPic(self):
        """Get your bot pic url"""
        return self.getdv("BOT_PIC") or self.BOT_PIC or "https://raw.githubusercontent.com/TronUb/Tron/master/main/core/resources/images/homepage.png" or None
