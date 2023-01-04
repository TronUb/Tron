import re
import copy
import inspect
import traceback

from typing import (
    Union, 
    List, 
    Pattern
)

from pyrogram.filters import create
from pyrogram import Client
from pyrogram.types import (
    Message, 
    CallbackQuery, 
    InlineQuery, 
    Update,
    User
)
from main.core.enums import (
    UserType,
    ChatType,
    SudoType
)



# custom regex filter
def regex(
    pattern: Union[str, Pattern], 
    flags: int = 0,
    allow: list = []
    ):

    async def func(flt, client: Client, update: Update):

        # work for -> sudo & bot owner if sudo
        if "sudo" in allow:
            if update.from_user and not (update.from_user.is_self or update.from_user.id in client.SudoUsers()):
                return False

            # allow some specific commands to sudos
            if update.from_user and update.from_user.id in client.SudoUsers():
                if update.text or update.caption and not "full" in client.SudoCmds():
                    for x in pattern.split(): # list of texts
                        if not x in client.SudoCmds():
                            return False

        # work only for -> bot owner if not sudo
        elif not "sudo" in allow:
            if update.from_user and not update.from_user.is_self:
                return False

        # work for -> forwarded message
        if not "forward" in allow:
            if update.forward_date: 
                return False

        # work for -> messages in channel
        if not "channel" in allow:
            if update.chat.type == "channel": 
                return False

        # work for -> edited message
        if not "edited" in allow:
            if update.edit_date: 
                return False

        if isinstance(update, Message):
            value = update.text or update.caption
        elif isinstance(update, CallbackQuery):
            value = update.data
        elif isinstance(update, InlineQuery):
            value = update.query
        else:
            raise ValueError(f"Regex filter doesn't work with {type(update)}")

        if value:
            update.matches = list(flt.p.finditer(value)) or None

        return bool(update.matches)

    return create(
        func,
        "RegexCommandFilter",
        p=pattern if isinstance(pattern, Pattern) else re.compile(pattern, flags)
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
    elif reply and message.reply:
        reply_attr = getattr(message.replied, reply_type)
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
    exclude: list = [],
    reply: bool = None,
    reply_type: list = None,
    disable_in: list = None,
    disable_for: list = None,
    sudo_type: "SudoType" = SudoType.COMMON,
    argcount: int = 0,
    **kwargs
    ):

    async def func(flt, client: Client, message: Message):

        try:
            text = message.text or message.caption or None
            message.command = None
            message.replied = message.reply_to_message
            user = getattr(message, "from_user", None)
            sudos = client.SudoUsers()

            if text is None:
                return False

            if message.forward_date: # forwarded messages can't be edited
                return False

            if message.chat.id in flt.disable_in:
                return False

            if user.id in flt.disable_for:
                return False

            flt.prefixes = client.Trigger() or ["."] # workaround

            for prefix in flt.prefixes:
                if not text.startswith(prefix):
                    continue

                cmd = text.split()[0][1:]
                if cmd in flt.commands:

                    dev_sudos = sudos.get("dev")
                    common_sudos = sudos.get("common")
                    sudo_users = dev_sudos.union(common_sudos)

                    if user.type == UserType.OWNER:
                        message.command = [cmd] + text.split()[1:]
                        message.sudo_message = None

                    elif user.type == UserType.SUDO:
                        if not message.from_user.sudo_type == sudo_type:
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

                        if not client.SudoCmds():
                            client.m = client.bot.m = message # remove later
                            return True

                        if not cmd in client.SudoCmds():
                            return False

                    else:
                        return False

                    client.m = client.bot.m = message # remove later

                    # reply condition
                    if not await is_reply(client, message, reply, reply_type):
                        return False

                    # max argument count condition 
                    if not await max_argcount(client, message, argcount):
                        return False

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
        "MessageCommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive,
        disable_in=disable_in,
        disable_for=disable_for,
        sudo_type=sudo_type
    )
