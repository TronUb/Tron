import threading

from sqlalchemy import (
    Column, 
    String, 
    Boolean, 
    UnicodeText, 
    Integer
)

from . import BASE, SESSION




MY_AFK = {}





class AFK(BASE):
    """ create table afk """
    __tablename__ = "afk"

    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean, default=False)
    reason = Column(UnicodeText, default=False)
    afktime = Column(Integer, default=0)

    def __init__(self, user_id, is_afk, reason, afktime):
        self.user_id = str(user_id)
        self.is_afk = is_afk
        self.reason = reason
        self.afktime = afktime

    def __repr__(self):
        return "<AFK {}>".format(self.user_id)




AFK.__table__.create(checkfirst=True)




class AFKSQL(object):
    """ AMC -> Afk Modification Class """
    def set_afk(self, afk, reason, afktime):
        global MY_AFK
        afk_db = SESSION.query(AFK).get(str(0))
        if afk_db:
            SESSION.delete(afk_db)
        afk_db = AFK(0, afk, reason, afktime)
        SESSION.add(afk_db)
        SESSION.commit()
        MY_AFK[0] = {"afk": afk, "reason": reason, "afktime": afktime}


    def get_afk(self):
        return MY_AFK.get(0)


    def load_afk():
        global MY_AFK
        try:
            MY_AFK = {}
            listall = SESSION.query(AFK).all()
            for x in listall:
                MY_AFK[(x.user_id)] = {"afk": x.is_afk, "reason": x.reason, "afktime": x.afktime}
        finally:
            SESSION.close()




AFKSQL.load_afk()

