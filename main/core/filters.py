import re
import copy
import inspect
import traceback

from typing import (
    Union, 
    List, 
    Pattern
)

from pyrogram.filters import *
from pyrogram import Client
from pyrogram.types import (
    Message, 
    CallbackQuery, 
    InlineQuery, 
    Update,
    User
)

from .types.superparser import SuperParser
from main.core.enums import (
    UserType,
    ChatType,
    SudoType
)




# gen reply checker
async def is_reply(client, message, reply, reply_type):
    if reply and not message.replied:
        await client.send_edit(
            "Reply to something . . .",
            text_type=["mono"],
            delme=3
        )
        return False
    elif reply and message.replied:
        if not reply_type:
            return True

        reply_attr = getattr(message.replied, reply_type, None)
        if reply_type and not reply_attr:
            await client.send_edit(
                f"Reply to {reply_type}",
                text_type=["mono"],
                delme=3
            )
            return False

    return True


# gen arguments count checker
async def max_argcount(client, message, argc):
    argc = 0 if argc is None else argc
    if argc <= 0:
        return True

    try:
        message.text.split()[argc]
    except IndexError:
        await client.send_edit(
            "Give me more arguments . . .",
            text_type=["mono"],
            delme=3
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
    **kwargs
    ):

    async def func(flt, client: Client, message: Message):

        try:
            if message is None:
                return False

            text = message.text or message.caption or None
            message.command = None
            message.replied = message.reply_to_message
            user = getattr(message, "from_user", None)

            if text is None:
                return False

            if user is None:
                return False

            if message.forward_date: # forwarded messages can't be edited
                return False

            if message.chat.id in flt.disable_in:
                return False

            if user.id in flt.disable_for:
                return False

            flt.prefixes = client.Trigger or ["."] # workaround

            for prefix in flt.prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text.split()[0][len(prefix):]
                for cmd in flt.commands:
                    if not re.match(
                        rf"\b{cmd}\b",
                        without_prefix,
                        flags=re.IGNORECASE if not 
                        flt.case_sensitive else 0
                        ):
                        continue

                    if user.type == UserType.OWNER:
                        message.command = [cmd] + text.split()[1:]
                        message.sudo_message = None

                    elif user.type == UserType.SUDO:
                        if not cmd in client.get_sudo(user.id).get("sudo_cmds"):
                            return False

                        new_message = await client.send_message(
                            message.chat.id,
                            "Hold on . . ."
                        )
                        if not new_message.from_user:
                            new_message.from_user = User(
                                id=client.id
                            )

                        setattr(new_message.from_user, "type", UserType.OWNER)
                        setattr(new_message, "sudo_message", copy.copy(message))

                        # update new attributes
                        message.__dict__ = new_message.__dict__

                        SuperParser.parse_combined_args(message)
                        return True
                    else:
                        return False

                    client.m = client.bot.m = message # remove later

                    # reply condition
                    if not await is_reply(client, message, flt.reply, flt.reply_type):
                        return False

                    # max argument count condition 
                    if not await max_argcount(client, message, flt.argcount):
                        return False

                    SuperParser.parse_combined_args(message)
                    return True

            return False
        except Exception as e:
            print(traceback.format_exc())

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    disable_in = [] if disable_in is None else disable_in
    disable_in = disable_in if isinstance(disable_in, list) else [disable_in]
    disable_in = set(disable_in) if disable_in else {""}

    disable_for = [] if disable_for is None else disable_for
    disable_for = disable_for if isinstance(disable_for, list) else [disable_for]
    disable_for = set(disable_for) if disable_for else {""}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

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
        argcount=argcount
    )
