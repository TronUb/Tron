import os
import platform




def clear():
	os.system("clear")



def create_termuxconfig():
	ATTR = ["API_ID", "API_HASH", "SESSION", "DB_URI", "LOG_CHAT", "TOKEN"]
	file = open("termuxconfig.py", "w+")
	file.write("class TermuxConfig:\n\ttemp = 'value'\n")
	for x in ATTR:
		if x == "DB_URI":
			value = _createdb()
		else:
			data = input(f"\nEnter your {x}: ")
			value = int(data) if data and data == "LOG_CHAT" else f"'{data}'"

		file.write(f"""\t{x.replace('"', "")} = {value}\n""")
	file.close()




def _startdb():
	if os.path.exists("/data/data/com.termux/files/usr/var/lib/postgresql"): 
		print("\nStarting postgres server.\n\n")
		os.system("pg_ctl -D $PREFIX/var/lib/postgresql restart")

	else:
		choice = input("\npostgres dependent file does not exist, enter all details again [y/n]: ")
		if choice in ("y", "Y", ""):
			clear()
			create_termuxconfig()
		else:
			print("Quiting process ...")
			os.system("cd ~")
			clear()




def _createdb():
	os.system("pkg install postgresql")
	clear()
	os.system("mkdir -p $PREFIX/var/lib/postgresql")
	os.system("initdb $PREFIX/var/lib/postgresql")
	clear()
	username = str(input("\nEnter your postgres account username: "))
	password = str(input("\nEnter your postgres account password: "))
	dbname = str(input("\nEnter your postgres database name: "))
	print("\n")
	os.system(f"createuser --superuser --pwprompt {username}")
	os.system(f"createdb {dbname}")
	os.system("pg_ctl -D $PREFIX/var/lib/postgresql restart")
	return f"'postgres://{username}:{password}@127.0.0.1:5432/{dbname}'"
