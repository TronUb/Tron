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
	
	chat_id = Column(String, primary_key=True)
	file_id = Column(String)
	text = Column(String)
	
	def __init__(self, user_id, file_id, text):
		self.chat_id = user_id
		self.file_id = file_id
		self.text = text




WELCOME.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




class WELCOMESQL(object):
	# set, del, get user_id & file_id
	def set_welcome(self, chat_id, file_id, text=None):
		with INSERTION_LOCK:
			mydata = SESSION.query(WELCOME).get(user_id)
			try:
				if mydata:
					SESSION.delete(mydata)
				mydata = WELCOME(chat_id, file_id, text)
				SESSION.add(mydata)
				SESSION.commit()
			finally:
				SESSION.close()
		return (chat_id, file_id, text)


	def del_welcome(self, chat_id):
		with INSERTION_LOCK:
			mydata = SESSION.query(WELCOME).get(chat_id)
			try:
				if mydata:
					SESSION.delete(mydata)
					SESSION.commit()
					SESSION.close()
					return True
			except Exception as e:
				SESSION.close()
				print(e)
				return False


	def get_welcome(self, chat_id):
		mydata = SESSION.query(WELCOME).get(chat_id)
		rep = None
		repx = None
		if mydata:
			rep = str(mydata.file_id)
			repx = mydata.text
		SESSION.close()
		return {"file_id" : rep, "caption" : repx}


	def get_welcome_ids(self):
		chat_ids = []
		all_welcome = SESSION.query(WELCOME).distinct().all()
		for x in all_welcome:
			if not int(x.chat_id) or x.chat_id in chat_ids:
				chat_ids.append(int(x.chat_id))
		SESSION.close()
		return chat_ids
		
