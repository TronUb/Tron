import threading

from sqlalchemy import (
    Column, 
    String, 
    Integer
)

from . import SESSION, BASE





class DVTABLE(BASE):
    __tablename__ = "Database Vars"

    keys = Column(String, primary_key=True)
    values = Column(String)
    
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values




DVTABLE.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()





class DVSQL(object):
    def setdv(self, keys: str, values: str):
        with INSERTION_LOCK:
            mydata = SESSION.query(DVTABLE).get(keys)
            try:
                if not mydata:
                    mydata = DVTABLE(keys, values)
                else:
                    mydata.values = values
                SESSION.merge(mydata)
                SESSION.commit()
            finally:
                SESSION.close()
        return keys


    def deldv(self, keys: str):
        with INSERTION_LOCK:
            mydata = SESSION.query(DVTABLE).get(keys)
            try:
                if mydata:
                    SESSION.delete(mydata)
                    SESSION.commit()
            finally:
                SESSION.close()
            return True


    def getdv(self, keys: str):
        mydata = SESSION.query(DVTABLE).get(keys)
        rep = ""
        if mydata:
            if mydata.values.isalnum():
                rep = str(mydata.values)
            else:
                rep = eval(str(mydata.values))
        SESSION.close()
        return rep


    def getalldv(self):
        kv_data = {}
        mydata = SESSION.query(DVTABLE).distinct().all()
        for x in mydata:
            kv_data.update({x.keys : x.values})

        return kv_data
