"""
Run after main.__init__.py, this file starts
and loads plugins for both assistant & userbot.
"""

import sys
import asyncio
import warnings
from pyrogram import idle
from pyrogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.errors import (
    PeerIdInvalid,
    ChannelInvalid
)
from main.userbot import app





async def start_assistant():
    """ this function starts the pyrogram bot client. """
    if app and app.bot:
        print("Activating assistant.\n")
        response = await app.bot.start()
        if response:
            print("Assistant activated.\n")
            botcmd = [
                ["start", "check whether bot is on or not."],
                ["help", "Get your helpdex."],
                ["ping", "Get server response speed & uptime."],
                ["id", "Get ids of users / groups."],
                ["quote", "get inline anime quotes."],
                ["broadcast", "send messages to users who have started your bot."],
                ["eval", "evaluate python codes."]
            ]
            cmds = [x.command for x in await app.bot.get_bot_commands()]
            botcmdkeys = [y[0] for y in botcmd]

            if cmds != botcmdkeys:
                print("Setting bot commands.\n")
                await app.bot.set_bot_commands([BotCommand(y[0], y[1]) for y in botcmd])
                print("Added bot commands.\n")
        else:
            print("Assistant is not activated.\n")
    else:
        print("Assistant start unsuccessful, please check that you have given the bot token.\n")
        print("skipping assistant start !")




async def start_userbot():
    """ this function starts the pyrogram userbot client. """
    if app:
        print("Activating userbot.\n")
        response = await app.start()
        if response:
            print("Userbot activated.\n")
        else:
            print("Userbot is not activated.\n")
    else:
        print("Userbot startup unsuccessful, please check everything again ...")
        print("Quiting ...")
        sys.exit()




async def send_start():
    await app.bot.send_message(
        app.LOG_CHAT,
        "The userbot is online now.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Support Group",
                        url="t.me/tronubsupport"
                    )
                ]
            ]
        )
    )




async def start_bot():
    """ This is the main startup function to start both clients i.e assistant & userbot.
    It also imports modules & plugins for assistant & userbot. """

    print(20*"_" + ". Welcome to Tron corporation ." + "_"*20 + "\n\n\n")
    print("PLUGINS: Installing.\n\n")
    botplugins = app.import_module("main/assistant/modules/plugins/", exclude=app.NoLoad())
    app.import_module("main/assistant/modules/callbacks/", display_module=False)
    app.import_module("main/assistant/modules/inlinequeries/", display_module=False)
    print(f"\n\n{botplugins} plugins Loaded\n\n")
    print("MODULES: Installing.\n\n")
    plugins = app.import_module("main/userbot/modules/plugins/", exclude=app.NoLoad())
    print(f"\n\n{plugins} modules Loaded\n\n")
    await start_assistant()
    await start_userbot()
    print("You successfully deployed Tronuserbot, try .ping or .alive commands to test it.")

    try:
        await send_start()
    except (ChannelInvalid, PeerIdInvalid):
        await app.get_chat(app.LOG_CHAT)
        await app.send_message(
            app.LOG_CHAT,
            "The userbot is online now."
        )

    await idle() # block execution



if __name__ == '__main__':
    with warnings.catch_warnings(): # suppress DeprecationWarning
        warnings.simplefilter("ignore")
        loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
