from pyrogram.types import Message as PyMessage
from pyrogram import raw
from .superparser import SuperParser




class Message(PyMessage):
    def __init__(id):
        super().__init__(id)

    @staticmethod
    async def parse(
        client: "pyrogram.Client",
        message: raw.base.Message,
        users: dict,
        chats: dict,
        is_scheduled: bool = False,
        replies: int = 1
        ):
        """ custome message parse method """
        r = await PyMessage._parse(
            client=client,
            message=message,
            users=users,
            chats=chats,
            is_scheduled=is_scheduled,
            replies=replies
        )

        return SuperParser.parse_user(client, r)
