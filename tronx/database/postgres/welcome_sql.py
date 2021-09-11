import threading

from sys import platform

from sqlalchemy import (
	Column, 
	String, 
	Integer
)

from . import SESSION, BASE




# save user ids in whitelists
class whole(BASE):
	__tablename__ = "welcome"
	
	keys = Column(String, primary_key=True)
	values = Column(String)
	
	def __init__(self, keys, values):
		self.keys = keys
		self.values = values




whole.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




# set, del, get keys & values
def set_welcome(keys, values):
	with INSERTION_LOCK:
		mydata = SESSION.query(whole).get(keys)
		try:
			if not mydata:
				mydata = whole(keys, values)
			else:
				mydata.values = values
			SESSION.merge(mydata)
			SESSION.commit()
		finally:
			SESSION.close()
	return keys




def del_welcome(keys):
	with INSERTION_LOCK:
		mydata = SESSION.query(whole).get(keys)
		try:
			if mydata:
				SESSION.delete(mydata)
				SESSION.commit()
		finally:
			SESSION.close()
		return False




def get_welcome(keys):
	mydata = SESSION.query(whole).get(keys)
	rep = ""
	if mydata:
		rep = str(mydata.values)
	SESSION.close()
	return rep




