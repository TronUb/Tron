from pyrogram.types import User as PyUser, Message
from main.core.enums import UserType
from pyrogram import Client


class SuperParser(PyUser):
    @staticmethod
    def parse_user(client: Client, message: Message) -> Message:
        """Parses user type based on sender information."""
        if not message or not message.from_user:
            return message  # Return message unchanged if invalid

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
        """Parses additional arguments for message processing."""
        if not message or not hasattr(message, "from_user"):
            return message  # Return if message is invalid

        message.combined_args = {}

        # Retrieve attributes safely with a fallback to sudo_message
        sm = getattr(message, "sudo_message", None)
        reply = getattr(message, "reply_to_message", None) or getattr(
            sm, "reply_to_message", None
        )
        command = getattr(message, "command", None) or getattr(sm, "command", None)

        # Update dictionary in one step for better performance
        message.combined_args.update(
            {"reply": reply, "reply_to_message": reply, "command": command}
        )

        return message
