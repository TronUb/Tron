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
        clear()
        print("Starting . . .\n\n")

    else:
        choice = input("\npostgres dependent file does not exist, enter all details again [y/N]: ")
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
    os.system(f"createdb u0_a402")
    os.system("pg_ctl -D $PREFIX/var/lib/postgresql restart")
    clear()
    return f"'postgres://u0_a402:trust@127.0.0.1:5432/u0_a402'"
