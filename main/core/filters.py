import copy
import re
import traceback
from typing import List, Union, Optional

from pyrogram import Client
from pyrogram.filters import *
from pyrogram.types import CallbackQuery, InlineQuery, Message, Update, User

from main.core.enums import ChatType, SudoType, UserType

from .types.superparser import SuperParser


# gen reply checker
async def is_reply(client, message, reply, reply_type):
    if reply and not message.replied:
        await client.send_edit("Reply to something . . .", text_type=["mono"], delme=3)
        return False
    elif reply and message.replied:
        if not reply_type:
            return True

        reply_attr = getattr(message.replied, reply_type, None)
        if reply_type and not reply_attr:
            await client.send_edit(
                f"Reply to {reply_type}", text_type=["mono"], delme=3
            )
            return False

    return True


async def max_argcount(
    client: Client, message: Message, argc: Optional[int] = None
) -> bool:
    """
    Checks if the message contains at least `argc` number of words.

    Parameters:
        client (Client): Pyrogram client instance.
        message (Message): Incoming message object.
        argc (Optional[int]): Minimum number of arguments required.

    Returns:
        bool: True if the message contains enough arguments, else False.
    """
    argc = argc or 0  # Ensure argc is an integer (default to 0)

    if argc <= 0:
        return True  # No argument limit, always return True

    # Check if the message has enough words
    words = message.text.split() if message.text else []

    if len(words) < argc:
        await client.send_edit(
            "Give me more arguments . . .", text_type=["mono"], delme=3
        )
        return False

    return True


# custom command filter
def gen(
    commands: Union[str, List[str]],
    prefixes: Union[str, List[str]] = [],
    case_sensitive: bool = True,
    reply: bool = None,
    reply_type: str = "",
    disable_in: list = None,
    disable_for: list = None,
    sudo_type: "SudoType" = SudoType.COMMON,
    argcount: int = 0,
    **kwargs,
):
    async def func(flt, client: Client, message: Message):
        try:
            if not message or not message.text:
                return False

            text = message.text or message.caption
            message.command = None
            message.replied = message.reply_to_message
            user = getattr(message, "from_user", None)

            if not user or message.forward_date:  # Ignore forwarded messages
                return False

            if message.chat.id in flt.disable_in or user.id in flt.disable_for:
                return False

            flt.prefixes = client.Trigger or ["."]  # Workaround for missing trigger

            for prefix in flt.prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text.split()[0][len(prefix):]

                for cmd in flt.commands:
                    if not re.match(
                        rf"\b{cmd}\b",
                        without_prefix,
                        flags=re.IGNORECASE if not flt.case_sensitive else 0,
                    ):
                        continue

                    if user.type == UserType.OWNER:
                        message.command = [cmd] + text.split()[1:]
                        message.sudo_message = None

                    elif user.type == UserType.SUDO:
                        if cmd not in client.get_sudo(user.id).get("sudo_cmds", []):
                            return False

                        new_message = await client.send_message(
                            message.chat.id, "Hold on . . ."
                        )
                        new_message.from_user = new_message.from_user or User(
                            id=client.id
                        )
                        setattr(new_message.from_user, "type", UserType.OWNER)
                        setattr(new_message, "sudo_message", copy.copy(message))

                        message.__dict__ = new_message.__dict__

                        SuperParser.parse_combined_args(message)
                        return True

                    else:
                        return False

                    client.m = client.bot.m = message  # Remove later if unnecessary

                    if not await is_reply(client, message, flt.reply, flt.reply_type):
                        return False

                    if not await max_argcount(client, message, flt.argcount):
                        return False

                    SuperParser.parse_combined_args(message)
                    return True

            return False

        except Exception:
            print(traceback.format_exc())

    commands = {
        c.lower() if not case_sensitive else c
        for c in (commands if isinstance(commands, list) else [commands])
    }
    disable_in = set(
        disable_in
        if isinstance(disable_in, list)
        else [disable_in] if disable_in else [""]
    )
    disable_for = set(
        disable_for
        if isinstance(disable_for, list)
        else [disable_for] if disable_for else [""]
    )
    prefixes = set(
        prefixes if isinstance(prefixes, list) else [prefixes] if prefixes else [""]
    )

    return create(
        func,
        "CustomMessageCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
        disable_in=disable_in,
        disable_for=disable_for,
        sudo_type=sudo_type,
        reply=reply,
        reply_type=reply_type,
        argcount=argcount,
    )
