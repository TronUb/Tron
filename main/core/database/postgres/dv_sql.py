import threading

from sqlalchemy import (
    Column, 
    String, 
    Integer
)

from . import SESSION, BASE





class DV(BASE):

    __tablename__ = "database var"
    
    keys = Column(String, primary_key=True)
    values = Column(String)
    
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values




DV.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()





class DVSQL(object):
    def setdv(self, keys, values):
        with INSERTION_LOCK:
            mydata = SESSION.query(DV).get(keys)
            try:
                if not mydata:
                    mydata = DV(keys, values)
                else:
                    mydata.values = values
                SESSION.merge(mydata)
                SESSION.commit()
            finally:
                SESSION.close()
        return keys


    def deldv(self, keys):
        with INSERTION_LOCK:
            mydata = SESSION.query(DV).get(keys)
            try:
                if mydata:
                    SESSION.delete(mydata)
                    SESSION.commit()
            finally:
                SESSION.close()
            return True


    def getdv(self, keys):
        mydata = SESSION.query(DV).get(keys)
        rep = ""
        if mydata:
            rep = str(mydata.values)
        SESSION.close()
        return rep


    def getalldv(self):
        kv_data = {}
        mydata = SESSION.query(DV).distinct().all()
        for x in mydata:
            kv_data.update({x.keys : x.values})

        return kv_data
