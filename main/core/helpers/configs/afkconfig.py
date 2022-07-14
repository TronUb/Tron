AFKDV = [
    "AFK_TEXT"
    ]




class AfkConfig(object):
    def AfkText(self):
        """ Set your custom afk texts """
        return self.getdv("AFK_TEXT") or self.AFK_TEXT  
