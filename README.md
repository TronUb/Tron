<p align="center">
    <a href="https://github.com/TronUb/Tron">
        <img src="main/others/resources/images/tron-round.png" height="300" width="300" alt="TronUb Logo">
    </a>
</p>

## Tron Userbot

![Repo Size](https://img.shields.io/github/repo-size/TronUb/Tron)
![License](https://img.shields.io/github/license/TronUb/Tron)
![Python Version](https://img.shields.io/badge/Python-3.9-aqua)
![Release](https://img.shields.io/github/v/release/TronUb/Tron)
![Maintained](https://img.shields.io/badge/Maintained%20%3F-Yes-orange)
![Files](https://img.shields.io/github/directory-file-count/TronUb/Tron?label=Repo%20Files)
![Commit since](https://img.shields.io/github/commits-since/TronUb/Tron/0.0.1/master)


## About

This is a Telegram userbot written in pure Python, based on [Pyrogram](https://github.com/pyrogram/pyrogram).

### What is a Userbot?

A userbot is a program that automates your Telegram account, similar to Telegram bots but operating through a user account. It can perform actions like downloading YouTube videos, creating stickers, preventing unknown users from messaging, image processing, and more. The functionality of a userbot can be extended indefinitely.

## Necessary Variables

```python
API_ID  # Get from https://my.telegram.org
API_HASH  # Get from https://my.telegram.org
SESSION  # Create a session using the methods below
LOG_CHAT  # Create a private group and get its chat ID
BOT_TOKEN  # Create a bot at https://t.me/BotFather and get its token
```

## Deployment Methods

### 1. Deploy on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### 2. Deploy on Local Machines

#### Windows

```shell
winget install -e --id Python.Python.3.10
python3 -m venv tronuserbot
tronuserbot/Scripts/activate
pip install setuptools
git clone https://github.com/TronUb/Tron
cd Tron
notepad .env  # Fill in the necessary details
python3 -m main
```

#### Linux

```shell
apt-get update -y && apt-get upgrade -y
apt-get install python3 -y
python3 -m venv tronuserbot
source tronuserbot/bin/activate
pip install setuptools
git clone https://github.com/TronUb/Tron
cd Tron
nano .env  # Fill in the necessary details
python3 -m main
```

### Environment Variables Format

```plaintext
API_ID=1234567
API_HASH=ad2gb7h9jd99jdu9bdid9jsh8s7h7eo9kbopz
SUDO_USERS=[1252773, 7737382, 1721726]
```

## Session Creation Methods

### 1. Repl.it Method

[![Repl.it](https://img.shields.io/badge/REPL%20RUN-Click%20Here-aqua.svg)](https://replit.com/@beastzx18/Tron-Userbot?v=1)

### 2. Termux Method

```shell
apt update && apt upgrade && pkg install python3 git
cd $HOME && git clone https://github.com/TronUb/Tron.git
cd Tron && python3 session.py
```

## Examples

```python
from main import app
from main.core import filters
from main.core.enums import HandlerType

# Userbot decorator
@app.on_update(
    handler_type=HandlerType.MESSAGE,
    filters=filters.gen(
        commands="check",
        usage="Check if bot is active."
    )
)
async def userbot_check_handler(client, message):
    await message.edit("Bot is Active!")

# Bot decorator
@app.bot.on_update(
    handler_type=HandlerType.MESSAGE,
    filters=filters.command(
        commands="check"
    )
)
async def bot_check_handler(bot, message):
    await bot.send_message(message.chat.id, "Bot is Active!")
```

## Support

## 🌍 Join the Community
[![Telegram](https://img.shields.io/badge/Telegram-Join%20Group-blue?logo=telegram)](https://t.me/tronuserbot)


## FAQ

Will be updated soon.

## Warning ⚠️

I am not responsible for any consequences of using this bot, including bans or restrictions on your account.

## Made With Fun By [࿇•ẞᗴᗩSԵ•࿇](https://t.me/beastzx)
Feel free to contribute and improve!
