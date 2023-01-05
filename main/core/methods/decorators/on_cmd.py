from typing import (
    List,
    Union,
    Callable
)

import pyrogram
import inspect
from main.core.enums import UserType
from main.core.filters import gen



class OnCmd:
    def on_cmd(
        self: "pyrogram.client",
        commands: Union[str, List[str]],
        prefixes: Union[str, List[str]] = None,
        module: str = None,
        usage: str = None,
        case_sensitive: bool = True,
        reply: bool = None,
        reply_type: Union["ReplyType", List["ReplyType"]] = None,
        disable_in: Union["ChatType", List["ChatType"]] = None,
        disable_for: Union["UserType", List["UserType"]] = UserType.OTHER,
        argcount: int = 0,
        group: int = 0
    ) -> Callable:

        command_info = {commands[0] if isinstance(commands, list) else commands : usage}
        cmd_help = self.CMD_HELP.get(module)
        if cmd_help:
            self.CMD_HELP.get(module).update(command_info)
        else:
            # wherever this decorator is called 
            # we will access its future local variables
            frame = inspect.currentframe().f_back
            module = frame.f_locals.get("__name__")
            print("module ", module)
            module_name = module.split(".")[-1]
            print("module_name ", module_name)

            cmd_help = self.CMD_HELP.get(module_name)
            print("cmd_help ", cmd_help)
            if cmd_help:
                self.CMD_HELP.get(module_name).update({command_info})

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