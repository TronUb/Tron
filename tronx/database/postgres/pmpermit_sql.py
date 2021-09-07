import threading

from sys import platform
from sqlalchemy import (
	Column, 
	String, 
	Integer
)

from . import SESSION, BASE




# save user ids in whitelists
class PMTable(BASE):
	__tablename__ = "approve"

	user_id = Column(Integer, primary_key=True)
	boolvalue = Column(String)

	def __init__(self, user_id, boolvalue):
		self.user_id = user_id
		self.boolvalue = boolvalue




# save warn msg ids
class MsgID(BASE):
	__tablename__ = "msgid_pm"

	user_id = Column(Integer, primary_key=True)
	msg_id = Column(Integer)

	def __init__(self, user_id, msg_id):
		self.user_id = user_id
		self.msg_id = msg_id




# save warn counts
class Disapprove(BASE):
	__tablename__ = "disapprove"

	user_id = Column(Integer, primary_key=True)
	warn_count = Column(Integer)

	def __init__(self, user_id, warn_count):
		self.user_id = user_id
		self.warn_count = warn_count




PMTable.__table__.create(checkfirst=True)
MsgID.__table__.create(checkfirst=True)
Disapprove.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




# add or remove msg id of a user
def set_msgid(user_id, msg_id):
	with INSERTION_LOCK:
		try:
			user = SESSION.query(MsgID).get(user_id)
			if not user:
				user = MsgID(user_id, msg_id)
			else:
				user.msg_id = msg_id
			SESSION.merge(user)
			SESSION.commit()
		finally:
			SESSION.close()




def get_msgid(user_id):
	try:
		user = SESSION.query(MsgID).get(user_id)
		msg_id = None
		if user:
			msg_id = user.msg_id
			return msg_id
	finally:
		SESSION.close()




# add or remove id from whitelist 
def set_whitelist(user_id, boolvalue):
	with INSERTION_LOCK:
		user = SESSION.query(PMTable).get(user_id)
		try:
			if not user:
				user = PMTable(user_id, boolvalue)
			else:
				user.boolvalue = str(boolvalue)
			SESSION.add(user)
			SESSION.commit()
		finally:
			SESSION.close()
	return user_id




def del_whitelist(user_id):
	with INSERTION_LOCK:
		user = SESSION.query(PMTable).get(user_id)
		try:
			if user:
				SESSION.delete(user)
				SESSION.commit()
		finally:
			SESSION.close()
		return False




def get_whitelist(user_id):
	user = SESSION.query(PMTable).get(user_id)
	rep = ""
	if user:
		rep = str(user.boolvalue)
	SESSION.close()
	return rep




# warn table func
def set_warn(user_id, warn_count):
	with INSERTION_LOCK:
		try:
			user = SESSION.query(Disapprove).get(user_id)
			if not user:
				user = Disapprove(user_id, warn_count)
			else:
				user.warn_count = warn_count
			SESSION.merge(user)
			SESSION.commit()
		finally:
			SESSION.close()




def get_warn(user_id):
	user = SESSION.query(Disapprove).get(user_id)
	rep = ""
	if user:
		rep = str(user.warn_count)
	SESSION.close()
	return rep

