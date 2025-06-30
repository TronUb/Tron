""" sudousers configuration module """

SUDOUSERSDV = [
    "SUDO_USERS",
    "SUDO_CMDS"
]


class SudoUsersConfig(object):
    @property
    def SudoAccess(self):
        return self.getdv("SUDO_ACCESS") or self.SUDO_ACCESS 

    @property
    def SudoUsers(self):
        """ returns the ids of all sudo profiles """
        return {x[0] for x in self.all_sudo().items()}

    @property
    def SudoUsersList(self):
        return list(self.SudoUsers)

    @property
    def SudoCmds(self):
        return self.getdv("SUDO_CMDS") or self.SUDO_CMDS
