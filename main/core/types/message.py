from pyrogram.types import Message as PyMessage
from pyrogram import raw
from .user import User




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

        if isinstance(r, raw.types.MessageEmpty):
            return None

        if not r.from_user:
            return None

        r = User.parse(client, r)

        return r
