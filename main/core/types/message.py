from typing import Optional, Dict, TYPE_CHECKING
from pyrogram.types import Message as PyMessage
from pyrogram import raw
from .superparser import SuperParser

if TYPE_CHECKING:
    from pyrogram.client import Client


class Message(PyMessage):
    """
    Custom wrapper over Pyrogram's Message with an extended static parser.
    """

    @staticmethod
    async def parse(
        client: "Client",
        message: raw.base.Message,
        users: Optional[Dict] = None,
        chats: Optional[Dict] = None,
        is_scheduled: bool = False,
        replies: int = 1,
    ) -> Optional[PyMessage]:
        """
        Parse a raw Telegram message into a Pyrogram Message, with user parsing.

        Args:
            client (Client): Pyrogram client instance.
            message (raw.base.Message): Raw Telegram message object.
            users (dict, optional): Users dictionary.
            chats (dict, optional): Chats dictionary.
            is_scheduled (bool, optional): Whether the message is scheduled.
            replies (int, optional): Reply count.

        Returns:
            Optional[PyMessage]: The fully parsed Pyrogram message object.
        """
        try:
            # Attempt to parse the raw message using Pyrogram internals
            parsed = await PyMessage._parse(
                client=client,
                message=message,
                users=users or {},
                chats=chats or {},
                is_scheduled=is_scheduled,
                replies=replies,
            )

            if parsed:
                # Add user-level metadata (your custom logic)
                parsed = SuperParser.parse_user(client, parsed)
                return parsed

            return None

        except Exception as e:
            print(f"[TronMessageParser] Failed to parse message: {e}")
            return None
