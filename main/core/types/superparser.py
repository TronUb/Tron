from pyrogram.types import User as BaseUser
from main.core.enums import UserType




class SuperParser(BaseUser):
    @staticmethod
    def parse_user(
        client,
        message
        ):
        """ custom user parser """
        if message and message.from_user:
            if message.from_user.is_self:
                message.from_user.type = UserType.OWNER
            elif message.from_user.id in client.SudoUsersList:
                message.from_user.type = UserType.SUDO
            else:
                message.from_user.type = UserType.OTHER

        return message


    @staticmethod
    def parse_combined_args(
        message
        ):
        """ custom combined args parser """
        if not (message or message.from_user):
            return message

        message.combined_args = dict()

        # shorten 
        sm = message.sudo_message
        mdict = message.combined_args

        # first priority to owner message attributes
        reply = getattr(message, "reply_to_message", None) or getattr(sm, "reply_to_message", None) 
        command = getattr(message, "command", None) or getattr(sm, "command", None)

        mdict.update(
            {"reply": reply}
        )
        mdict.update(
            {"reply_to_message": reply}
        )
        mdict.update(
            {"command": command}
        )

        return message