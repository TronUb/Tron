import os
import time
import requests
import json
import threading

from sqlalchemy import (
	Column, 
	UnicodeText, 
	Integer, 
	String
)

from tronx.helpers.utils import Types

from . import SESSION, BASE




class sudolist(BASE):
	__tablename__ = "sudolist"

	index = Column(Integer, primary_key=True)
	user_id = Column(String)

	def __init__(self, user_id, index):
		self.user_id = user_id
		self.index = index

	def __repr__(self):
		return "<Sudo %s>" % self.name

sudolist.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()




# save sudo users
def save_sudo(user_id, index=0): # use user_id in square brackets    
	with INSERTION_LOCK:
		prev = SESSION.query(sudolist).get(index)
		if prev:
			data = prev + [user_id]
			SESSION.delete(prev)
			again = sudolist(data, index)
		else:
			again = sudolist(user_id, index)
		SESSION.add(again)
		SESSION.commit()
		return True




# get a saved sudo users
def get_sudo(index=0):
	prev = SESSION.query(sudolist).get(index)
	if prev:
		return prev
	else:
		return False


def del_sudo(sudo_id, index=0):
	prev = SESSION.query(sudolist).get(index)
	if prev:
		data = list(set(prev) - set(sudo_id)) # remove multiple common elements 
		SESSION.delete(prev)
		next_data = sudolist(data, index)
		SESSION.add(next_data)
		SESSION.commit()
		return True
	else:
		return "sudolist is empty"
