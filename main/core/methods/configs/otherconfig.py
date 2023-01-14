""" otherconfig configuration module """

OTHERDV = [
    "NO_LOAD",
    "SUDO_USERS",
    "SUDO_CMDS",
    "PREFIX",
    "HELP_EMOJI",
    "SPOTIFY_TOKEN"
    ]



class OtherConfig(object):
    @property
    def NoLoad(self):
        """ Get your No load module list """
        noload_plugins = self.getdv("NO_LOAD")
        noload_list = noload_plugins.split() if noload_plugins else None
        return noload_list or self.NO_LOAD or []


    @property
    def AllUsersId(self):
       """ Returns owner id & sudo users id as a list """
       return [self.id] + self.SudoUsersList


    @property
    def Trigger(self):
        """ Get list of prefixes (command handlers) """
        trigger = self.getdv("TRIGGER")
        return trigger.split() if trigger else None or self.TRIGGER.split() or "."


    @property
    def HelpEmoji(self):
        """ This will return the emoji which will be used in helpdex """
        return self.getdv("HELP_EMOJI") or self.HELP_EMOJI or ""


    @property
    def SpotifyToken(self):
        """ returns your spotify token """
        return self.getdv("SPOTIFY_TOKEN") or self.SPOTIFY_TOKEN or {}


    @property
    def LogChat(self):
        """ returns your log chat id """
        return self.getdv("LOG_CHAT") or self.LOG_CHAT or None
