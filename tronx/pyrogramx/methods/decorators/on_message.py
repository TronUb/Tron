from typing import Callable

import pyrogram
from pyrogram.filters import Filter
from pyrogram.scaffold import Scaffold



class OnMessage(Scaffold):
	def on_message(
		self = None,
		filters = None,
		group: int = 0
	) -> callable:
		"""Decorator for handling messages : (user defined method)."""

		def decorator(func: Callable) -> Callable:
			if isinstance(self, pyrogram.Client):
				self.add_handler(pyrogram.handlers.MessageHandler(func, filters), group)
			elif isinstance(self, Filter) or self is None:
				if not hasattr(func, "handlers"):
					func.handlers = []

				func.handlers.append(
					(
						pyrogram.handlers.MessageHandler(func, self),
						group if filters is None else filters
					)
				)

			return func

		return decorator
