import threading
from sqlalchemy import Column, String, Boolean, UnicodeText, Integer
from . import BASE, SESSION

# In-memory AFK cache
MY_AFK = {}

# pylint: disable=no-member

class AFK(BASE):
    """AFK Table Definition"""
    __tablename__ = "afk"

    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean, default=False)
    reason = Column(UnicodeText, default="")
    afktime = Column(Integer, default=0)

    def __init__(self, user_id, is_afk=False, reason="", afktime=0):
        self.user_id = str(user_id)
        self.is_afk = is_afk
        self.reason = reason
        self.afktime = afktime

    def __repr__(self):
        return f"<AFK {self.user_id}>"


# Create table if it doesn't exist
AFK.__table__.create(checkfirst=True)


class AFKSQL:
    """Afk Management Helper"""

    @staticmethod
    def set_afk(user_id: int, afk: bool, reason: str, afktime: int):
        global MY_AFK
        user_id = str(user_id)
        try:
            existing = SESSION.query(AFK).get(user_id)
            if existing:
                SESSION.delete(existing)

            new_afk = AFK(user_id=user_id, is_afk=afk, reason=reason, afktime=afktime)
            SESSION.add(new_afk)
            SESSION.commit()
            MY_AFK[user_id] = {"afk": afk, "reason": reason, "afktime": afktime}
        finally:
            SESSION.close()

    @staticmethod
    def get_afk(user_id: int):
        return MY_AFK.get(str(user_id), None)

    @classmethod
    def load_afk(cls):
        global MY_AFK
        MY_AFK = {}
        try:
            records = SESSION.query(AFK).all()
            for x in records:
                MY_AFK[x.user_id] = {
                    "afk": x.is_afk,
                    "reason": x.reason,
                    "afktime": x.afktime,
                }
        finally:
            SESSION.close()


# Initial load
AFKSQL.load_afk()
