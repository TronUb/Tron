""" userbot client module """

import random
import string
from pyrogram import Client
from main.assistant.client import Bot
from main.core import Core
from main.core.newpyrogram.dispatcher import Dispatcher



# temp -
random_name =  "".join(random.choices(string.ascii_uppercase + string.digits, k = 7))


class SuperClient(Core, Client):
    """ Userbot (tron) """
    def __init__(self):
        super().__init__(
            name=random_name,
            api_id=self.API_ID,
            api_hash=self.API_HASH,
            session_string=self.SESSION,
            workers=self.WORKERS,
        )
        self.start()
        self.me = self.get_chat("me")
        self.id = self.me.id
        self.dc_id = self.me.dc_id
        self.first_name = self.me.first_name
        self.last_name = self.me.last_name if self.me.last_name else ""
        self.name = self.first_name + " " + self.last_name
        self.username = f"@{self.me.username}" if self.me.username else ""
        self.bio = self.me.bio if self.me.bio else ""
        self.pic = self.download_media(self.me.photo.big_file_id) if self.me.photo else None
        self.is_bot = False
        self.stop()
        self.bot = Bot()
        self.dispatcher = Dispatcher(self)
        self.__class__.__module__ = "pyrogram.client"
