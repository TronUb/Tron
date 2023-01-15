""" userbot client module """

import os
from pyrogram import (
    Client,
    idle,
    handlers
)
from pyrogram.raw.types import (
    UpdateNewMessage,
    UpdateNewChannelMessage,
    UpdateNewScheduledMessage
)
from pyrogram.errors import (
    PeerIdInvalid,
    ChannelInvalid
)

from main.others.colors import Colors
from main.assistant.client import Bot
from main.core import Core
from main.core.types import Message




NEW_MESSAGE_UPDATES = (
    UpdateNewMessage,
    UpdateNewChannelMessage,
    UpdateNewScheduledMessage
)


class SuperClient(Core, Client):
    """ Userbot (tron) """
    def __init__(self):
        super().__init__(
            name="tronuserbot",
            api_id=self.API_ID,
            api_hash=self.API_HASH,
            session_string=self.SESSION,
            workers=self.WORKERS,
        )
        # start the bot and setup whatever needed
        # before other classes start requesting that
        # information which is not available at the 
        # moment & stop it to start it later
        self.start()
        self.me = self.get_chat("me")
        self.id = self.me.id
        self.dc_id = self.me.dc_id
        self.first_name = self.me.first_name
        self.last_name = self.me.last_name if self.me.last_name else ""
        self.name = self.first_name + " " + self.last_name
        self.username = f"@{self.me.username}" if self.me.username else ""
        self.bio = self.me.bio if self.me.bio else ""

        # reduce the profile image downloading
        dp_name = f"dp_{self.id}.jpg"
        dp_path = f"./downloads/{dp_name}"
        if not os.path.exists(dp_path):
            self.pic = self.download_media(self.me.photo.big_file_id, dp_name) if self.me.photo else None 

        self.stop()
        self.is_bot = None

        # start the bot by initialising 
        self.bot = Bot()
        self.__class__.__module__ = "pyrogram.client"

        # set custom message parser
        for parser in NEW_MESSAGE_UPDATES:
            self.dispatcher.update_parsers.update({
                parser:self.message_parser
            })

        # update plugin names with empty dicts in CMD_HELP
        for file in os.listdir("main/userbot/modules/plugins/"):
            if not file.startswith("__"):
                self.CMD_HELP.update({file.split(".")[0]:{}})


    async def message_parser(self, update, users, chats):
        """ custom message parser """
        return (
            await Message.parse(
                self,
                update.message,
                users,
                chats,
                isinstance(
                    update,
                    UpdateNewScheduledMessage
                )
            ),
            handlers.MessageHandler
        )


    async def start_userbot(self):
        """ this function starts the pyrogram userbot client. """
        if not self:
            raise Exception("The userbot client is missing.")
            quit(0)

        print(f"{Colors.block}Userbot  :{Colors.reset} [{Colors.red}OFF{Colors.reset}]{Colors.reset}")
        response = await self.start()
        if response:
            print(Colors.cursor_up(2))
            print(f"{Colors.block}Userbot  :{Colors.reset} [{Colors.green}ON{Colors.reset}] {Colors.reset}", end="\n\n")
        else:
            print("Userbot is not activated.\n")


    async def start_bot(self):
        """ This is the main startup function to start both clients i.e assistant & userbot.
        It also imports modules & plugins for assistant bot & userbot. """

        try:
            print(20*"_" + Colors.block + Colors.bold + ". Welcome to Tron corporation ." + Colors.reset + "_"*20 + "\n\n\n")

            print(Colors.block + "PLUGINS:" + Colors.reset + " ( Assistant )\n\n")
            botplugins = self.import_module("main/assistant/modules/plugins/", exclude=self.NoLoad)
            self.import_module("main/assistant/modules/callbacks/", display_module=False)
            self.import_module("main/assistant/modules/inlinequeries/", display_module=False)
            print(f"\n\n{Colors.block}Total plugins:{Colors.reset} {botplugins}\n\n\n")

            print(Colors.block + "PLUGINS:" + Colors.reset + " ( Userbot )\n\n")
            ubotplugins = self.import_module("main/userbot/modules/plugins/", exclude=self.NoLoad)
            print(f"\n\n{Colors.block}Total plugins:{Colors.reset} {ubotplugins}\n")

            await self.bot.start_assistant()
            await self.start_userbot()
            print("You successfully deployed Tronuserbot, try .ping or .alive commands to test it.")

            try:
                await self.send_start_message()
            except (ChannelInvalid, PeerIdInvalid):
                print("Userbot start message wasn't send in Log Chat.")

            await idle() # block execution
        except Exception:
            print(traceback.format_exc())
