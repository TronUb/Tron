from typing import (
    List,
    Union,
    Callable
)

import pyrogram
from main.core.enums import UserType



class OnCmd:
    def on_cmd(
        self: "pyrogram.client",
        commands: Union[str, List[str]],
        module: str,
        prefixes: Union[str, List[str]] = None,
        usage: str = None,
        case_sensitive: bool = True,
        reply: bool = None,
        reply_type: Union["ReplyType", List["ReplyType"]] = None,
        disable_in: Union["ChatType", List["ChatType"]] = None,
        disable_for: Union["UserType", List["UserType"]] = UserType.OTHER,
        argcount: int = None,
        group: int = 0
    ) -> Callable:

        command_info = {command[0] if isinstance(command, list) else command : usage}
        cmd_help = self.CMD_HELP.get(module)
        if cmd_help:
            cmd_help.update(command_info)
        else:
            self.CMD_HELP.update({module: command_info})

        disable_in = disable_in if isinstance(disable_in, list) else [disable_in]
        disable_for = disable_for if isinstance(disable_for, list) else [disable_for]
        reply_type = reply_type if isinstance(reply_type, list) else [reply_type]

        def decorator(func: Callable) -> Callable:
            if not isinstance(self, pyrogram.Client):
                raise Exception("Instance should be pyrogram.Client in on_cmd decorator.")
            self.add_handler(
                pyrogram.handlers.MessageHandler(
                    func,
                    gen(
                        commands=commands,
                        prefixes=prefixes,
                        disable_in=disable_in,
                        disable_for=disable_for,
                        case_sensitive=case_sensitive,
                        reply=reply,
                        reply_type=reply_type,
                        argcount=argcount
                    )
                ),
                group
            )

            return func

        return decorator