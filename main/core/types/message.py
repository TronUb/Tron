from pyrogram.types import Message as BaseMessage
from pyrogram import raw
from main.core.enums import UserType



class Message(BaseMessage):
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
        r = await BaseMessage._parse(
            client=client,
            message=message,
            users=users,
            chats=chats,
            is_scheduled=is_scheduled,
            replies=replies
        )
        
        if not (r or r.from_user):
            return r
        
        user = r.from_user
        if user.is_self:
            user.type = UserType.OWNER
        elif user.id in client.SudoUsersList():
            user.type = UserType.SUDO
        else:
            user.type = UserType.OTHER
            
        return r
        