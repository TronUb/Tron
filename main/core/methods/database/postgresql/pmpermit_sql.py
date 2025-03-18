import threading

from sqlalchemy import Column, String, Integer

from . import SESSION, BASE


# save user ids in whitelists
class PMTABLE(BASE):
    __tablename__ = "approve"

    user_id = Column(Integer, primary_key=True)
    boolvalue = Column(String)

    def __init__(self, user_id, boolvalue):
        self.user_id = user_id
        self.boolvalue = boolvalue


# save warn msg ids
class MSGID(BASE):
    __tablename__ = "pm msg id"

    user_id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)

    def __init__(self, user_id, msg_id):
        self.user_id = user_id
        self.msg_id = msg_id


# save warn counts
class DISAPPROVE(BASE):
    __tablename__ = "disapprove"

    user_id = Column(Integer, primary_key=True)
    warn_count = Column(Integer)

    def __init__(self, user_id, warn_count):
        self.user_id = user_id
        self.warn_count = warn_count


PMTABLE.__table__.create(checkfirst=True)  # pylint: disable=E1101
MSGID.__table__.create(checkfirst=True)  # pylint: disable=E1101
DISAPPROVE.__table__.create(checkfirst=True)  # pylint: disable=E1101

INSERTION_LOCK = threading.RLock()

session = SESSION()


class PMPERMITSQL(object):
    # add message id of a user
    def set_msgid(self, user_id, msg_id):
        with INSERTION_LOCK:
            try:
                user = session.query(MSGID).get(user_id)
                if not user:
                    user = MSGID(user_id, msg_id)
                else:
                    user.msg_id = msg_id
                session.merge(user)
                session.commit()
            finally:
                session.close()

    # get warn message id
    def get_msgid(self, user_id):
        try:
            user = session.query(MSGID).get(user_id)
            msg_id = None
            if user:
                msg_id = user.msg_id
                return msg_id
        finally:
            session.close()

    # add user id to whitelist
    def set_whitelist(self, user_id, boolvalue):
        with INSERTION_LOCK:
            user = session.query(PMTABLE).get(user_id)
            try:
                if not user:
                    user = PMTABLE(user_id, boolvalue)
                else:
                    user.boolvalue = str(boolvalue)
                session.add(user)
                session.commit()
            finally:
                session.close()
        return user_id

    # remove user id from whitelist
    def del_whitelist(self, user_id):
        with INSERTION_LOCK:
            user = session.query(PMTABLE).get(user_id)
            try:
                if user:
                    session.delete(user)
                    session.commit()
            finally:
                session.close()
            return False

    # get whitelist (approved)
    def get_whitelist(self, user_id):
        user = session.query(PMTABLE).get(user_id)
        rep = ""
        if user:
            rep = str(user.boolvalue)
        session.close()
        return rep

    # warn table func
    def set_warn(self, user_id, warn_count):
        with INSERTION_LOCK:
            try:
                user = session.query(DISAPPROVE).get(user_id)
                if not user:
                    user = DISAPPROVE(user_id, warn_count)
                else:
                    user.warn_count = warn_count
                session.merge(user)
                session.commit()
            finally:
                session.close()

    # get warn func
    def get_warn(self, user_id):
        user = session.query(DISAPPROVE).get(user_id)
        rep = ""
        if user:
            rep = str(user.warn_count)
        session.close()
        return rep

    # del warn func
    def del_warn(self, user_id):
        with INSERTION_LOCK:
            user = session.query(DISAPPROVE).get(user_id)
            try:
                if user:
                    session.delete(user)
                    session.commit()
            finally:
                session.close()
            return False
