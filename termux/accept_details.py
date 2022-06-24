import os
from .database import createdb




def configfile():
	file = open("config.py", "w+")
	return file


file = configfile()


def ask_information():
	file.write("class Config:\n") 
	db_url = createdb()
	file.write(f"\tDB_URI = '{db_url}'")

	# api id
	API_ID = api_id()
	if API_ID:
		file.write(f"\tAPI_ID = {API_ID}\n")      
	else:
		quit(0)

	# api hash
	API_HASH = api_hash()
	if API_HASH:
		file.write(f"\tAPI_HASH = '{API_HASH}'\n")      
	else:
		quit(0)

	# session
	SESSION = session()
	if SESSION:
		file.write(f"\tSESSION = '{SESSION}'\n")      
	else:
		quit(0)

	# bot token
	BOT_TOKEN = bot_token()
	if BOT_TOKEN:
		file.write(f"\tBOT_TOKEN = '{BOT_TOKEN}'\n")      
	else:
		quit(0)

	# prefix
	PREFIX = prefix()
	if PREFIX:
		file.write(f"\tPREFIX = '{PREFIX}'\n")      
	else:
		quit(0)

	# log chat
	LOG_CHAT = log_chat()
	if LOG_CHAT:
		file.write(f"\tLOG_CHAT = '{LOG_CHAT}'\n")      
	else:
		quit(0)

	file.close()


def api_id():
	data = input("\nEnter your API_ID: ")
	if (not data) or (not data.isdigit()):
		print("\nEnter valid details\n")
		api_id()

	return data if data else None



def api_hash():
	data = input("\nEnter your API_HASH: ")
	if not data:
		print("\nEnter valid details\n")
		api_hash()

	return data if data else None


def session():
	data = input("\nEnter your SESSION: ")
	if not data:
		print("\nEnter valid details\n")
		session()

	return data if data else None


def bot_token():
	data = input("\nEnter your TOKEN: ")
	if not data:
		print("\nEnter valid details\n")
		bot_token()

	return data if data else None


def prefix():
	data = input("\nEnter your PREFIX: ")
	if not data:
		print("\nEnter valid details\n")
		prefix()

	return data if data else None


def log_chat():
	data = input("\nEnter your LOG_CHAT: ")
	if not data:
		print("\nEnter valid details\n")
		log_chat()

	return data if data else None













