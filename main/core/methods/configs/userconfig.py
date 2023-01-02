
USERDV = [
    "USER_NAME",
    "USER_USERNAME",
    "USER_ID",
    "USER_PIC",
    "USER_BIO"
    ]



class UserConfig(object):
    def UserName(self):
        """returns name of user"""
        return self.getdv("USER_NAME") or self.USER_NAME or self.name or None


    def UserUsername(self):
        """returns username of user"""
        return self.getdv("USER_USERNAME") or self.USER_USERNAME or self.username or None


    def UserMention(self):
        """returns mention of user"""
        return self.MentionMarkdown(self.UserId(), self.UserName()) if self.UserName() and self.UserId() else None


    def UserId(self):
        """returns telegram id of user"""
        return self.getdv("USER_ID") or self.USER_ID or self.id or None


    def UserDc(self):
        """returns telegram dc id of user"""
        return self.getdv("DC_ID") or self.dc_id or None


    def UserPic(self):
        """returns pic of user"""
        return self.getdv("USER_PIC") or self.USER_PIC or self.pic or None


    def UserBio(self):
        """returns bio of user"""
        return self.getdv("USER_BIO") or self.USER_BIO or self.bio or None
