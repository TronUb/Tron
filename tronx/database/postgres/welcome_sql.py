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
	
	user_id = Column(String, primary_key=True)
	file_id = Column(String)
	text = Column(String)
	
	def __init__(self, user_id, file_id, text):
		self.user_id = user_id
		self.file_id = file_id
		self.text = text




whole.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




# set, del, get user_id & file_id
def set_welcome(user_id, file_id, text=None):
	with INSERTION_LOCK:
		mydata = SESSION.query(whole).get(user_id)
		try:
			if not mydata:
				mydata = whole(user_id, file_id, text)
			else:
				mydata.file_id = file_id
			SESSION.merge(mydata)
			SESSION.commit()
		finally:
			SESSION.close()
	return user_id




def del_welcome(user_id):
	with INSERTION_LOCK:
		mydata = SESSION.query(whole).get(user_id)
		try:
			if mydata:
				SESSION.delete(mydata)
				SESSION.commit()
		finally:
			SESSION.close()
		return False




def get_welcome(user_id):
	mydata = SESSION.query(whole).get(user_id)
	rep = ""
	if mydata:
		rep = str(mydata.file_id)
		repx = str(mydata.text)
	SESSION.close()
	return rep, repx




