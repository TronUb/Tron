import threading

from sqlalchemy import (
	Column, 
	String, 
	Integer
)

from . import SESSION, BASE




# save user ids in whitelists
class WELCOME(BASE):
	__tablename__ = "welcome"
	
	user_id = Column(String, primary_key=True)
	file_id = Column(String)
	text = Column(String)
	
	def __init__(self, user_id, file_id, text):
		self.user_id = user_id
		self.file_id = file_id
		self.text = text




WELCOME.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




class WELCOMESQL(object):
	# set, del, get user_id & file_id
	def set_welcome(self, user_id, file_id, text=None):
		with INSERTION_LOCK:
			mydata = SESSION.query(WELCOME).get(user_id)
			try:
				if mydata:
					SESSION.delete(mydata)
				mydata = WELCOME(user_id, file_id, text)
				SESSION.add(mydata)
				SESSION.commit()
			finally:
				SESSION.close()
		return user_id


	def del_welcome(self, user_id):
		with INSERTION_LOCK:
			mydata = SESSION.query(WELCOME).get(user_id)
			try:
				if mydata:
					SESSION.delete(mydata)
					SESSION.commit()
			finally:
				SESSION.close()
			return False


	def get_welcome(self, user_id):
		mydata = SESSION.query(WELCOME).get(user_id)
		rep = None
		repx = None
		if mydata:
			rep = str(mydata.file_id)
			repx = mydata.text
		SESSION.close()
		return {"file_id" : rep, "caption" : repx}

	def get_welcome_all(self):
		kv_data = {}
		all_welcome = SESSION.query(WELCOME).distinct().all()
		for x in all_welcome:
			kv_data.update({"chat_id" : x.user_id, "file_id" : x.file_id, "text" : x.text})
		SESSION.close()
		return dict(kv_data)
		
