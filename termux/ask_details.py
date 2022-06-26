import os
import platform




def clear():
	osname = platform.uname()[0]
	return "cls" if osname == "Windows" else "clear"



def create_termuxconfig():
	ATTR = ["API_ID", "API_HASH", "SESSION", "DB_URI", "LOG_CHAT", "TOKEN"]
	file = open("termuxconfig.py", "w+")
	file.write("class Termuxconfig:\n\ttemp = 'value'\n")
	for x in ATTR:
		myvar = vars() # string to variable
		if x == "DB_URI":
			value = createdb()
		else:
			data = input(f"\nEnter your {x}: ")
			value = int(data) if data and data == "LOG_CHAT" else f"'{data}'"
		

		myvar[x] = value
		file.write(f"""\t{x.replace('"', "")} = {value}\n""")
	file.close()
	return True



def startdb():
	if os.path.exists("/data/data/com.termux/files/usr/var/lib/postgresql"):
		os.system("pg_ctl -D $PREFIX/var/lib/postgresql start")

	else:
		try:
			from termuxconfig import Termuxconfig
		except (ImportError, ModuleNotFoundError):
			os.system("cd ~ && cd Tron && ./start.sh")

		try:
			Termuxconfig.DB_URI
		except AttributeError:
			file = open("termuxconfig.py", "a")
			file.write(f"\tDB_URI = {create_db()}\n")
			file.close()



def createdb():
	os.system("pkg install postgresql")
	os.system(clear())
	os.system("mkdir -p $PREFIX/var/lib/postgresql")
	os.system("initdb $PREFIX/var/lib/postgresql")
	os.system(clear())
	username = str(input("\nEnter your database account username: "))
	password = str(input("\nEnter your database account password: "))
	dbname = str(input("\nEnter your database name: "))
	print("\n")
	os.system(f"createuser --superuser --pwprompt {username}")
	os.system(f"createdb {dbname}")
	os.system("pg_ctl -D $PREFIX/var/lib/postgresql start")
	return f"'postgres://{username}:{password}@127.0.0.1:5432/{dbname}'"
