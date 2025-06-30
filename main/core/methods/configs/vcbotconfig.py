""" bot configuration module """



VCBOTDV = [
    "VCBOT",
    "VC_ACCESS"
]


class VcBotConfig(object):
    """ bot configuration module """
    def VcBot(self):
        """ Get your bot name """
        return self.getdv("VCBOT") or self.VCBOT or None

    def VcBotAccess(self):
        """ Allow people to use bot publically """
        return self.getdv("VCBOT_ACCESS") or self.VCBOT_ACCESS or None
