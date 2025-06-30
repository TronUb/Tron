from pyrogram.types import User as PyUser, Message
from pyrogram import Client
from main.core.enums import UserType


class SuperParser(PyUser):
    """
    Utilities to enhance and parse incoming message/user data.
    """

    @staticmethod
    def parse_user(client: Client, message: Message) -> Message:
        """
        Assigns a custom user type to the message sender based on their role.
        """
        if not message or not message.from_user:
            return message

        user = message.from_user

        if user.is_self:
            user.type = UserType.OWNER
        elif user.id in getattr(client, "SudoUsersList", []):
            user.type = UserType.SUDO
        else:
            user.type = UserType.OTHER

        return message

    @staticmethod
    def parse_combined_args(message: Message) -> Message:
        """
        Adds `.combined_args` to the message, consolidating reply and command data.
        Useful for simplified plugin logic.
        """
        if not message or not hasattr(message, "from_user"):
            return message

        sudo_msg = getattr(message, "sudo_message", None)
        reply = getattr(message, "reply_to_message", None) or getattr(
            sudo_msg, "reply_to_message", None
        )
        command = getattr(message, "command", None) or getattr(
            sudo_msg, "command", None
        )

        message.combined_args = {
            "reply": reply,
            "reply_to_message": reply,
            "command": command,
        }

        return message
