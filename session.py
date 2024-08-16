"""Generates a string session for the Tron Userbot
"""

import platform
import subprocess
from os import system

def clear_screen():
    "clears the screen"
    r = platform.system().lower()
    command = "clear" if r == "linux" or r == "darwin" else "cls" if r == "windows" else ""
    subprocess.run(command.split(), capture_output=True, text=True, check=True)

try:
    system("python3 -m pip install pyrogram")
    from pyrogram import Client
except Exception:
    print("Couldn't install pyrogram")

# Useful information before doing anything
INTRO = """
@Tronuserbot Corporation
Get the following values by logging to,

https://my.telegram.org

Requirements:

  1. API_ID
  2. API_HASH
  3. PHONE NUMBER (WITH COUNTRY CODE, EX: +911034567891)

  NOTE: Enter "Ctrl + C" to exit
\n
"""


print(INTRO)


while True:
    API_ID = input("Enter your API_ID: ")

    if not (API_ID and len(API_ID) == 7):
        print("\n\nPlease enter a valid 7 digit API ID.\n\n")
        continue
    break

while True:
    API_HASH = input("Enter API HASH: ")
    if not API_HASH:
        print("\n\nPlease enter a valid API HASH.\n\n")
        continue
    break


# create a new pyrogram session
with Client(
    name="tronbot",
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True
    ) as app:
    session = app.export_session_string()
    app.send_message(
        "me",
        f"""This Is Your Tron Userbot • [ `SESSION` ]\n\n{session}
        ⚠️• Don't share this with anyone !!
        Create session online • [ Press Here ](https://replit.com/@beastzx18/Tron-Userbot-Session)""",
        disable_web_page_preview=True
    )
    print(session)
    print("\n\nYour String Session Is Successfully Saved In Telegram Saved (Cloud) Messages !! Don't Share It With Anyone!! Anyone having your session can use (Hack) your Telegram Account !")
