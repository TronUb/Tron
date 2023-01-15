"""
This file creates Assistant's client.
"""

import os
import traceback

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import BotCommand

from main.others.colors import Colors
from main.core import Core




class Bot(Core, Client):
    """ Assistant (Nora) """
    def __init__(self):
        super().__init__(
            name="Nora",
            api_id=self.API_ID,
            api_hash=self.API_HASH,
            bot_token=self.BOT_TOKEN
    )
        try:
            self.start()
            self.me = self.get_chat("me")
            self.id = self.me.id
            self.dc_id = self.me.dc_id
            self.name = self.me.first_name
            self.username = f"@{self.me.username}"
            self.bio = self.me.bio if self.me.bio else ""
            dp_name = f"dp_{self.id}.jpg"
            dp_path = f"./downloads/{dp_name}"
            if not os.path.exists(dp_path):
                self.pic = self.download_media(self.me.photo.big_file_id, dp_name) if self.me.photo else None
            self.is_bot = True
            self.stop()
        except FloodWait as e:
            print(e)

        self.__class__.__module__ = "pyrogram.client"


    async def start_assistant(self):
        """ this function starts the pyrogram bot client. """

        try:
            if not self:
                raise Exception("The userbot client is missing.")
                quit(0)

            if not self.is_bot:
                raise Exception("The assistant client is missing.")
                quit(0)

            print(f"{Colors.block}Assistant:{Colors.reset} [{Colors.red}OFF{Colors.reset}]{Colors.reset}")
            response = await self.start()
            if response:
                # move cursor one line up
                print(Colors.cursor_up(2))
                print(f"{Colors.block}Assistant:{Colors.reset} [{Colors.green}ON{Colors.reset}] {Colors.reset}", end="\n\n")
                botcmd = [
                    ["start", "check whether bot is on or not."],
                    ["help", "Get your helpdex."],
                    ["ping", "Get server response speed & uptime."],
                    ["id", "Get ids of users / groups."],
                    ["quote", "get inline anime quotes."],
                    ["broadcast", "send messages to users who have started your bot."],
                    ["eval", "evaluate python codes."]
                ]
                cmds = [x.command for x in await self.get_bot_commands()]
                botcmdkeys = [y[0] for y in botcmd]

                if cmds != botcmdkeys:
                    print("Setting bot commands.\n")
                    await self.set_bot_commands([BotCommand(y[0], y[1]) for y in botcmd])
                    print("Added bot commands.\n")
            else:
                print("Assistant is not activated.\n")
        except Exception:
            print(traceback.format_exc())
