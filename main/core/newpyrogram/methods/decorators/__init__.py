from .on_message import OnMessage
from .on_callback import OnCallbackQuery
from .on_inline import OnInlineQuery



class Decorators(
	OnMessage,
	OnInlineQuery,
	OnCallbackQuery,
):
	pass
