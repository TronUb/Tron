from typing import Optional, Dict
from pyrogram.types import Message as PyMessage
from pyrogram import raw
from .superparser import SuperParser


class Message(PyMessage):

    def __init__(self):
        """Custom Message class inheriting Pyrogram's Message"""
        super().__init__(id=id)

    @staticmethod
    async def parse(
        client: "pyrogram.Client",
        message: raw.base.Message,
        users: Optional[Dict] = None,
        chats: Optional[Dict] = None,
        is_scheduled: bool = False,
        replies: int = 1,
    ) -> Optional[PyMessage]:
        """
        Custom message parsing method.

        Parameters:
            client (pyrogram.Client): Pyrogram client instance.
            message (raw.base.Message): Raw Telegram message data.
            users (dict, optional): Dictionary of users.
            chats (dict, optional): Dictionary of chats.
            is_scheduled (bool, optional): If the message is scheduled.
            replies (int, optional): Number of replies.

        Returns:
            Optional[PyMessage]: Parsed message or None if parsing fails.
        """
        try:
            # Parse the raw message
            r = await PyMessage._parse(
                client=client,
                message=message,
                users=users or {},
                chats=chats or {},
                is_scheduled=is_scheduled,
                replies=replies,
            )

            if r:
                # Further parse user details
                parsed_message = SuperParser.parse_user(client, r)
                client.message = parsed_message  # Store in client for global access
                return parsed_message

            return None  # Return None if parsing fails

        except Exception as e:
            # Log errors if any
            print(f"Error parsing message: {e}")
            return None
