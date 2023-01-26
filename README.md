<p align="center">
    <a href="https://github.com/beastzx18/Tron">
        <img src="main/others/resources/images/tron-round.png" height="300" width="300" alt="TronUb">
    </a>
</p>

<h2 align="center">Tron Userbot</h2> 

![Repo Size](https://img.shields.io/github/repo-size/TronUb/Tron)
![License](https://img.shields.io/github/license/TronUb/Tron)
![Python Version](https://img.shields.io/badge/python-3.x.x-aqua)
![Release](https://img.shields.io/github/v/release/TronUb/Tron)
![Maintained](https://img.shields.io/badge/Maintained%20%3F-Yes-orange)
![Files](https://img.shields.io/github/directory-file-count/TronUb/Tron?label=repo%20files)
![Commit since](https://img.shields.io/github/commits-since/TronUb/Tron/0.0.1/master)


<h2>click below to expand</h2>

<details>
    <summary><b>• About</b></summary>

<br />
<b>This is a telegram userbot which is written in pure python language and it is based on Dan's</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a> <b>library.</b>

<b>Now let's understand what is a userbot ?</b>

<b>A userbot is simple program to automate your telegram account. Userbots are same as telegram bots.</b>
<b>the difference is that all the functionality & features of a bot is provided in a telegram user account.</b>

<b>You might be thinking, what can a userbot do ? well userbots can do a lots of things for example downloading a video/audio from
YouTube, making telegram stickers, stopping unknown users from messaging us, image processing, etc. A userbot is not limited
to its features it can be extended more and more, it can do more beyond its limits.</b>

</details>


<details>
    <summary>
        <b>• Necessary vars</b>
    </summary>
<br></br>

```python
API_ID
# get this value from https://my.telegram.org

API_HASH
# get this value from https://my.telegram.org

SESSION
# create session from session methods given below 

TRIGGER
# by default its dot (.) 
# change it to any single symbol you like

LOG_CHAT
# make a private group and get its chat id

TIME_ZONE
# by default its Asia/Kolkata, change it 
# your time zone

BOT_TOKEN
# create a bot at https://t.me/BotFather 
# and get its bot token
```

</details>


<details>
    <summary><b>• Deployment ( 2 methods )</b></summary>

<br />

<b>1. Deploy on Heroku</b>

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

---

<br />

<b>2. Deploy on Local Machine</b>


• <i>Windows:</i>

1. Install python ```winget install -e --id Python.Python.3.10```

2. Create virtual environment ```python -m venv tronuserbot```

3. Activate the virtual environment ```tronuserbot/Scripts/activate```

4. Go to home path ```cd```

5. Install git ```winget install -e --id Git.Git```

6. Clone tronuserbot repo ```git clone https://github.com/TronUb/Tron```

7. change directory ```cd Tron```

8. Start the tronuserbot installation setup ```python -m main```


• <i>Linux:</i>

1. Update and upgrade ```apt-get update && apt-get upgrade```

2. Install python ```apt-get install python```

3. Create python virtual environment ```python -m venv tronuserbot```

4. Activate python virtual environment ```source tronuserbot/bin/activate```

5. Install git ```apt-get install git```

6. Clone tronuserbot repo ```git clone https://github.com/TronUb/Tron```

7. Change directory ```cd Tron```

8. Paste your keys and values in config.text file ```nano config.text```

9. After pasting all of your information, use <b>Ctrl + X</b> and enter <b>Y</b> and again hit enter button.

10. Start the tronuserbot installation setup ```python -m main```


<b>Note:</b> You have to add keys & values in config.txt file same as given below 👇

```API_ID=1234567```<br />
```API_HASH=ad2gb7h9jd99jdu9bdid9djd9jsh8s7h7eo9kbopz```<br />
```SUDO_USERS=[1252773, 7737382, 1721726]```

<p>🎉 Done, Have fun using tronuserbot.</p>

---

<br />
</details>

<details>
<summary><b>• Session ( 2 methods )</b></summary>

<br />
<b>1. Repl method</b>

[![Repl.it](https://img.shields.io/badge/REPL%20RUN-Click%20Here-aqua.svg)](https://replit.com/@beastzx18/Tron-Userbot?v=1)

---

<br />

<b>2. Termux method</b>

* Run the given command in termux

``` shell
apt update && apt upgrade && pkg install python3 git && cd $HOME && git clone https://github.com/TronUb/Tron.git && cd Tron && python3 session.py 
```

---

<br />
</details>

<details>
    <summary>
        <b>• Examples</b>
    </summary>

``` python3
from main import app
from main.core import filters
from main.core.enums import HandlerType


@app.on_update(
    handler_type=HandlerType.MESSAGE,
    filters=filters.gen(
        commands="check",
        usage="Check Bot is active or not."
    )
)
async def check_handler(client, message):
    await message.edit("Bot is Active !")

# The gen filter is only made for userbot
```
</details>

<b>Warning ⚠️:</b>
I will not be responsible for anything that happens with your account, channels, groups, friends, etc, if you get banned or limited it will be your fault, most of time nothing happens. 

<br />

• MADE WITH 🎉 BY [࿇•ẞᗴᗩSԵ•࿇](https://t.me/beastzx)
