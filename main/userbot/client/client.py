""" userbot client module """

import os
import pyrogram
from pyrogram import Client
from main.assistant.client import Bot
from main.core import Core
from pyrogram.raw.types import (
    UpdateNewMessage,
    UpdateNewChannelMessage,
    UpdateNewScheduledMessage
)
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
            pyrogram.handlers.MessageHandler
        )