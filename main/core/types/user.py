from pyrogram.types import User as BaseUser
from main.core.enums import UserType




class User(BaseUser):
    def __init__(id):
        super().__init__(id)

    @staticmethod
    def parse(
        client,
        message
        ):
        if message.from_user.is_self:
            message.from_user.type = UserType.OWNER
        elif message.from_user.id in client.SudoUsersList:
            message.from_user.type = UserType.SUDO
        else:
            message.from_user.type = UserType.OTHER

        return message