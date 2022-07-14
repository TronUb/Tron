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
            continue
            data = input(f"\nEnter your {x}: ")
            value = int(data) if data and data == "LOG_CHAT" else f"'{data}'"

        file.write(f"""\t{x.replace('"', "")} = {value}\n""")
    file.close()
