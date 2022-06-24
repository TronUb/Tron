import os



def configfile():
	file = open("config.py", "w+")
	return file


file = configfile()


def ask_information():
	if api_id():
		file.write(f"API_ID = {api_id()}\n")      
	else:
		quit(0)

	if api_hash():
		file.write(f"API_HASH = {api_hash()}\n")      
	else:
		quit(0)

	if session():
		file.write(f"SESSION = {session()}\n")      
	else:
		quit(0)

	if bot_token():
		file.write(f"BOT_TOKEN = {bot_token()}\n")      
	else:
		quit(0)

	if prefix():
		file.write(f"PREFIX = {prefix()}\n")      
	else:
		quit(0)

	if log_chat():
		file.write(f"LOG_CHAT = {log_chat()}\n")      
	else:
		quit(0)


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













