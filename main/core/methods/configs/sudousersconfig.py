import json

SUDOUSERSDV = [
    "SUDO_USERS",
    "SUDO_CMDS"
]


class SudoUsersConfig(object):
    @property
    def SudoUsers(self):
        """ returns the return value of dv.getdv for SUDO_USERS """
        return self.getdv("SUDO_USERS")

    @property
    def SudoUsersDev(self):
        """ returns dev sudo user ids """
        return self.SudoUsers.get("dev")

    @property
    def SudoUsersCommon(self):
        """ returns common sudo user ids """
        return self.SudoUsers.get("common")

    @property
    def SudoUsersAll(self):
        """ returns all sudo users ids as set """
        return self.SudoUsers.get("dev").union(
            self.SudoUsers.get("common")
        )

    @property
    def SudoUsersAllList(self):
        """ returns all sudo users ids as list """
        return list(self.SudoUsersAll)

    @property
    def SudoCmds(self):
        """ returns a list of plugin command names """
        sudo_cmds = self.getdv("SUDO_CMDS")
        return sudo_cmds.split() if sudo_cmds else []
