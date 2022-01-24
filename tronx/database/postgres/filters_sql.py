import threading

from sqlalchemy import (
	Column, 
	String, 
	Integer
)

from . import SESSION, BASE




class FILTERS(BASE):
	__tablename__ = "filters"
	
	trigger = Column(String, primary_key=True)
	chat_id = Column(String)
	file_id = Column(String)
	caption = Column(String)
	
	def __init__(self, trigger, chat_id, file_id, caption):
		self.trigger = trigger
		self.chat_id = chat_id
		self.file_id = file_id
		self.caption = caption




FILTERS.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




class FILTERSSQL(object):
	def set_filter(self, trigger, chat_id, file_id, caption=False):
		with INSERTION_LOCK:
			mydata = SESSION.query(filters).get(trigger)
			try:
				if mydata:
					SESSION.delete(mydata)
				mydata = filters(trigger, chat_id, file_id, caption)
				SESSION.add(mydata)
				SESSION.commit()
			finally:
				SESSION.close()
		return chat_id




	def del_filter(self, trigger):
		with INSERTION_LOCK:
			mydata = SESSION.query(filters).get(trigger) 
			try:
				if mydata:
					SESSION.delete(mydata)
					SESSION.commit()
			finally:
				SESSION.close()
			return False




	def get_filter(self, trigger):
		mydata = SESSION.query(filters).get(trigger)
		rep = None
		repx = None
		repy = None
		repz = None
		if mydata:
			rep = str(mydata.file_id)
			repx = mydata.trigger
			repy = mydata.chat_id
			repz = mydata.caption
		SESSION.close()
		return {"file_id" : rep, "trigger" : repx, "chat_id" : repy, "caption" : repz}




