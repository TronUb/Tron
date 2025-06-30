import copy
import re
import traceback
from typing import List, Union, Optional

from pyrogram import Client
from pyrogram.filters import create
from pyrogram.types import CallbackQuery, InlineQuery, Message, Update, User

from main.core.enums import ChatType, SudoType, UserType
from .types.superparser import SuperParser


# --- Reply check ---
async def is_reply(client, message, reply_required, reply_type):
    if reply_required and not message.replied:
        await client.send_edit("Reply to something . . .", text_type=["mono"], delme=3)
        return False

    if reply_required and reply_type:
        reply_attr = getattr(message.replied, reply_type, None)
        if not reply_attr:
            await client.send_edit(
                f"Reply to {reply_type}", text_type=["mono"], delme=3
            )
            return False

    return True


# --- Argument count check ---
async def max_argcount(client: Client, message: Message, argc: int = 0) -> bool:
    if argc <= 0:
        return True

    words = message.text.split() if message.text else []
    if len(words) < argc:
        await client.send_edit(
            "Give me more arguments . . .", text_type=["mono"], delme=3
        )
        return False

    return True


# --- Main custom command filter ---
def gen(
    commands: Union[str, List[str]],
    prefixes: Union[str, List[str]] = [],
    case_sensitive: bool = True,
    reply: Optional[bool] = None,
    reply_type: str = "",
    disable_in: Optional[List[int]] = None,
    disable_for: Optional[List[int]] = None,
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

            if not user or message.forward_date:
                return False  # Ignore forwards or invalid sender

            if message.chat.id in flt.disable_in or user.id in flt.disable_for:
                return False

            flt.prefixes = client.Trigger or ["."]

            for prefix in flt.prefixes:
                if not text.startswith(prefix):
                    continue

                raw_command = text.split()[0][len(prefix) :]

                for cmd in flt.commands:
                    if not re.match(
                        rf"\b{cmd}\b",
                        raw_command,
                        flags=re.IGNORECASE if not flt.case_sensitive else 0,
                    ):
                        continue

                    # OWNER
                    if user.type == UserType.OWNER:
                        message.command = [cmd] + text.split()[1:]
                        message.sudo_message = None

                    # SUDO
                    elif user.type == UserType.SUDO:
                        sudo_data = client.get_sudo(user.id)
                        if cmd not in sudo_data.get("sudo_cmds", []):
                            return False

                        sudo_msg = await client.send_message(
                            message.chat.id, "Hold on . . ."
                        )
                        sudo_msg.from_user = sudo_msg.from_user or User(id=client.id)

                        setattr(sudo_msg.from_user, "type", UserType.OWNER)
                        setattr(sudo_msg, "sudo_message", copy.copy(message))

                        message.__dict__ = sudo_msg.__dict__

                    # Not sudo or owner
                    else:
                        return False

                    client.m = client.bot.m = message  # Optional shared context

                    if not await is_reply(client, message, flt.reply, flt.reply_type):
                        return False

                    if not await max_argcount(client, message, flt.argcount):
                        return False

                    SuperParser.parse_combined_args(message)
                    return True

            return False

        except Exception:
            print(traceback.format_exc())

    # Normalize filter attributes
    commands = {
        c.lower() if not case_sensitive else c
        for c in (commands if isinstance(commands, list) else [commands])
    }
    disable_in = set(disable_in or [])
    disable_for = set(disable_for or [])
    prefixes = set(
        prefixes if isinstance(prefixes, list) else [prefixes] if prefixes else []
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
