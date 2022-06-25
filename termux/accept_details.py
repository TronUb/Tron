import os



def create_termuxconfig():
	ATTR = ["API_ID", "API_HASH", "SESSION", "DB_URI", "LOG_CHAT", "TOKEN"]
	file = open("termuxconfig.py", "w+")
	file.write("class Termuxconfig:\n\ttemp = 'value'")
	for x in ATTR:
		myvar = vars() # string to variable
		data = input(f"\nEnter your {x}: ")
		value = f"{data}" if data == "LOG_CHAT" else f"'{data}'"
		if data == "DB_URI":
			value = createdb()

		file.write(f"\tmyvar[x] = {value}\n")
	file.close()
	return True




def createdb():
	os.system("pkg install postgresql")
	os.system("clear")

	if os.path.exists("$PREFIX/var/lib/postgresql"):
		os.system("pg_ctl -D $PREFIX/var/lib/postgresql start")
		return None
	else:
		os.system("mkdir -p $PREFIX/var/lib/postgresql")
		os.system("initdb $PREFIX/var/lib/postgresql")
		username = str(input("\nEnter your database account username: "))
		password = str(input("\nEnter your database account password: "))
		dbname = str(input("\nEnter your database name: "))
		print("\n")
		os.system(f"createuser --superuser --pwprompt {username}")
		os.system(f"createdb {dbname}")
		os.system("pg_ctl -D $PREFIX/var/lib/postgresql start")
		return f"'postgres://{username}:{password}@127.0.0.1:5432/{dbname}'"
