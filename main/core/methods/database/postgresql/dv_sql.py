import threading

from sqlalchemy import Column, String, Integer

from . import SESSION, BASE


class DVTABLE(BASE):
    __tablename__ = "Database Vars"

    keys = Column(String, primary_key=True)
    values = Column(String)

    def __init__(self, keys, values):
        self.keys = keys
        self.values = values


DVTABLE.__table__.create(checkfirst=True)  # pylint: disable=E1101

INSERTION_LOCK = threading.RLock()

session = SESSION()

class DVSQL(object):
    def setdv(self, keys: str, values: str):
        with INSERTION_LOCK:
            mydata = session.query(DVTABLE).get(keys)
            try:
                if not mydata:
                    mydata = DVTABLE(keys, values)
                else:
                    mydata.values = values
                session.merge(mydata)
                session.commit()
            finally:
                session.close()
        return keys

    def deldv(self, keys: str):
        with INSERTION_LOCK:
            mydata = session.query(DVTABLE).get(keys)
            try:
                if mydata:
                    session.delete(mydata)
                    session.commit()
            finally:
                session.close()
            return True

    def getdv(self, keys: str):
        mydata = session.query(DVTABLE).get(keys)
        rep = ""
        if mydata:
            if mydata.values.isalnum():
                rep = str(mydata.values)
            else:
                rep = eval(str(mydata.values))
        session.close()
        return rep

    def getalldv(self):
        kv_data = {}
        mydata = session.query(DVTABLE).distinct().all()
        for x in mydata:
            kv_data.update({x.keys : x.values})

        return kv_data
