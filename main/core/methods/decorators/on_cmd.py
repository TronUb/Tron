import inspect
from typing import Callable, List, Optional, Union

import pyrogram

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
        Decorator for handling command-based message handlers in Pyrogram.

        Parameters:
            commands (str | List[str]): Command names.
            prefixes (str | List[str], optional): Command prefixes.
            module (str, optional): Module name.
            usage (str, optional): Command usage information.
            case_sensitive (bool, optional): If True, commands are case-sensitive.
            reply (bool, optional): Whether the command should send a reply.
            reply_type (ReplyType, optional): The type of reply.
            disable_in (ChatType | List[ChatType], optional): Chat types where command is disabled.
            disable_for (UserType | List[UserType], optional): User types for which the command is disabled.
            argcount (int, optional): Number of arguments the command expects.
            group (int, optional): Group number for handler execution.

        Returns:
            Callable: The decorated function.
        """
        if isinstance(commands, str):
            commands = [commands]

        if not commands:
            raise ValueError("At least one command must be provided.")

        command_info = {commands[0]: usage}

        # Update command help documentation
        if module:
            self.CMD_HELP.setdefault(module, {}).update(command_info)
        else:
            frame = inspect.currentframe().f_back
            module_name = frame.f_locals.get("__name__")

            if module_name:
                module_key = module_name.split(".")[-1]
                self.CMD_HELP.setdefault(module_key, {}).update(command_info)
            else:
                raise RuntimeError("Failed to determine the module name.")

        # Ensure disable_in and disable_for are lists
        disable_in = (
            [disable_in] if isinstance(disable_in, ChatType) else (disable_in or [])
        )
        disable_for = (
            [disable_for] if isinstance(disable_for, UserType) else (disable_for or [])
        )

        def decorator(func: Callable) -> Callable:
            if not isinstance(self, pyrogram.Client):
                raise TypeError("Instance must be pyrogram.Client in on_cmd decorator.")

            handler = pyrogram.handlers.MessageHandler(
                func,
                gen(
                    commands=commands,
                    prefixes=prefixes,
                    disable_in=disable_in,
                    disable_for=disable_for,
                    case_sensitive=case_sensitive,
                    reply=reply,
                    reply_type=reply_type,
                    argcount=argcount,
                ),
            )

            self.add_handler(handler, group)
            return func

        return decorator
