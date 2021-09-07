import threading

from sys import platform

from sqlalchemy import (
	Column, 
	String, 
	Integer
)

from . import SESSION, BASE




# save user ids in whitelists
class data(BASE):
	__tablename__ = "database_var"
	
	keys = Column(String)
	values = Column(String)
	
	def __init__(self, keys, values):
		self.keys = keys
		self.values = values




data.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




# set, del, get keys & values
def setdv(keys, values):
	with INSERTION_LOCK:
		mydata = SESSION.query(data).get(keys)
		try:
			if not mydata:
				user = data(keys, values)
			else:
				user.values = str(values)
			SESSION.add(user)
			SESSION.commit()
		finally:
			SESSION.close()
	return keys




def deldv(keys):
	with INSERTION_LOCK:
		mydata = SESSION.query(data).get(keys)
		try:
			if mydata:
				SESSION.delete(mydata)
				SESSION.commit()
		finally:
			SESSION.close()
		return False




def getdv(keys):
	mydata = SESSION.query(data).get(keys)
	rep = ""
	if mydata:
		rep = str(mydata.value)
	SESSION.close()
	return rep




