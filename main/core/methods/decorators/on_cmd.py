import inspect
from typing import Callable, List, Optional, Union

import pyrogram
from pyrogram.handlers import MessageHandler

from main.core.enums import UserType, ChatType, ReplyType
from main.core.filters import gen


# pylint: disable=E1101
class OnCmd:
    def on_cmd(
        self: "pyrogram.Client",
        commands: Union[str, List[str]],
        prefixes: Optional[Union[str, List[str]]] = None,
        module: Optional[str] = None,
        usage: Optional[str] = None,
        case_sensitive: bool = True,
        reply: Optional[bool] = None,
        reply_type: Optional["ReplyType"] = None,
        disable_in: Optional[Union["ChatType", List["ChatType"]]] = None,
        disable_for: Union["UserType", List["UserType"]] = UserType.OTHER,
        argcount: int = 0,
        group: int = 0,
    ) -> Callable:
        """
        Register a command handler with detailed control over behavior.

        Args:
            commands: Command(s) to trigger.
            prefixes: Allowed command prefixes (defaults to client.Trigger).
            module: Module name for help documentation.
            usage: Help string for this command.
            case_sensitive: Whether command matching is case sensitive.
            reply: Require a reply to the message.
            reply_type: Enforce the type of reply (e.g., TEXT, PHOTO).
            disable_in: Disables this command in specific chat types.
            disable_for: Disables this command for user types.
            argcount: Minimum number of required arguments.
            group: Handler group.

        Returns:
            Callable: A decorator for the command function.
        """
        if isinstance(commands, str):
            commands = [commands]

        if not commands:
            raise ValueError("At least one command must be provided.")

        # Update CMD_HELP registry
        cmd_help_key = (
            module
            or inspect.stack()[1]
            .frame.f_globals.get("__name__", "unknown")
            .split(".")[-1]
        )
        self.CMD_HELP.setdefault(cmd_help_key, {}).update(
            {commands[0]: usage or "No description provided."}
        )

        # Normalize inputs
        disable_in = (
            [disable_in] if isinstance(disable_in, ChatType) else (disable_in or [])
        )
        disable_for = (
            [disable_for] if isinstance(disable_for, UserType) else (disable_for or [])
        )

        def decorator(func: Callable) -> Callable:
            if not isinstance(self, pyrogram.Client):
                raise TypeError(
                    "Decorator can only be used on pyrogram.Client instances."
                )

            self.add_handler(
                MessageHandler(
                    func,
                    gen(
                        commands=commands,
                        prefixes=prefixes,
                        case_sensitive=case_sensitive,
                        reply=reply,
                        reply_type=reply_type,
                        disable_in=disable_in,
                        disable_for=disable_for,
                        argcount=argcount,
                    ),
                ),
                group=group,
            )
            return func

        return decorator
