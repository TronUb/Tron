import json

OTHERDV = [
    "NO_LOAD",
    "SUDO_USERS",
    "SUDO_CMDS",
    "PREFIX",
    "HELP_EMOJI",
    "SPOTIFY_TOKEN"
    ]



class OtherConfig(object):
    def NoLoad(self):
        """ Get your No load module list """
        noload_plugins = self.getdv("NO_LOAD")
        noload_list = noload_plugins.split() if noload_plugins else None
        return noload_list or self.NO_LOAD or [] 


    def SudoUsers(self):
        """ Get sudo users """
        sudo_users = self.getdv("SUDO_USERS")
        if sudo_users:
            sudo_users = json.loads(sudo_users)
            sudo_types = {
                "common": set(int(x) for x in sudo_users.get("common")),
                "dev": set(int(x) for x in sudo_users.get("dev"))
            }
        else:
            sudo_types = None
        return sudo_types or {"dev": {}, "common": set(int(x) for x in self.SUDO_USERS)} or {}



    def Trigger(self):
        """ Get list of prefixes (command handlers) """
        trigger = self.getdv("TRIGGER")
        return trigger.split() if trigger else None or self.TRIGGER.split() or "."


    def HelpEmoji(self):
        """ This will return the emoji which will be used in helpdex """
        return self.getdv("HELP_EMOJI") or self.HELP_EMOJI or ""


    def SudoCmds(self):
        """ returns a list of command names """
        sudo_cmds = self.getdv("SUDO_CMDS")
        return sudo_cmds.split() if sudo_cmds else []


    def SpotifyToken(self):
        """ returns your spotify token """
        return self.getdv("SPOTIFY_TOKEN") or self.SPOTIFY_TOKEN or {}



