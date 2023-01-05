from pyrogram.types import Message as BaseMessage
from pyrogram.types import User as BaseUser
from pyrogram import raw
from main.core.enums import UserType, SudoType



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

        sudos = client.SudoUsers()

        if r.from_user is None:
            # to do
            r.from_user = BaseUser(
                id=0000000000,
                is_self=False
            )
            return r

        user = r.from_user
        if user.is_self:
            user.type = UserType.OWNER
        elif user.id in client.SudoUsersList():
            user.type = UserType.SUDO
            if user.id in sudos.get("dev"):
                user.sudo_type = SudoType.DEV
            elif user.id in sudos.get("common"):
                user.sudo_type = SudoType.COMMON
            else:
                user.sudo_type = SudoType.UNKNOWN
        else:
            user.type = UserType.OTHER

        return r
