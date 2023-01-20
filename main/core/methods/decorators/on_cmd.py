import inspect
import pyrogram

from typing import (
    List,
    Union,
    Callable
)

from main.core.enums import UserType
from main.core.filters import gen



class OnCmd:
    def on_cmd(
        self: "pyrogram.client",
        commands: Union[str, List[str]] = None,
        prefixes: Union[str, List[str]] = None,
        module: str = None,
        usage: str = None,
        case_sensitive: bool = True,
        reply: bool = None,
        reply_type: "ReplyType" = None,
        disable_in: Union["ChatType", List["ChatType"]] = None,
        disable_for: Union["UserType", List["UserType"]] = UserType.OTHER,
        argcount: int = 0,
        group: int = 0
    ) -> Callable:

        command_info = {commands[0] if isinstance(commands, list) else commands : usage}
        
        if module:
            if not module in self.CMD_HELP.keys():
                self.CMD_HELP.update({module : {}})
            self.CMD_HELP.get(module).update(command_info)
        else:
            # wherever this decorator is called 
            # we will access its future local variables
            frame = inspect.currentframe().f_back
            module = frame.f_locals.get("__name__")

            self.CMD_HELP.get(module.split(".")[-1]).update(command_info)

        disable_in = disable_in if isinstance(disable_in, list) else [disable_in]
        disable_for = disable_for if isinstance(disable_for, list) else [disable_for]

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

