import os
from config import Config




def createdb():
	db = True
	try:
		Config.DB_URI
	except AttributeError:
		db = False

	if not db:
		os.system("pkg install postgresql")
		os.system("clear")
		os.system("mkdir -p $PREFIX/var/lib/postgresql")
		os.system("initdb $PREFIX/var/lib/postgresql")
		os.system("pg_ctl -D $PREFIX/var/lib/postgresql start")
		username = str(input("\nEnter your database account username: "))
		password = str(input("\nEnter your database account password: "))
		dbname = str(input("\nEnter your database name: "))
		os.system(f"createuser --superuser --pwprompt {username}")
		os.system(f"createdb {dbname}")
		return f"postgres://{username}:{password}@127.0.0.1:5432/{dbname}"
	return None
