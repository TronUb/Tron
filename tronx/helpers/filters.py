import os
import re
import time

from typing import (
	Union, 
	List, 
	Dict, 
	Pattern
)

from pyrogram.filters import create
from pyrogram import filters, Client
from pyrogram.types import (
	Message, 
	CallbackQuery, 
	InlineQuery, 
	InlineKeyboardMarkup, 
	ReplyKeyboardMarkup, 
	Update
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




# custom command filter
def gen(
	commands: Union[str, List[str]], 
	prefixes: Union[str, List[str]] = [],
	case_sensitive: bool = True, 
	allow: list = []
	):

	# modified function of pyrogram.filters.command
	command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
	async def func(flt, client: Client, message: Message):

		start = time.time()
		text = message.text or message.caption
		message.command = None
		user = message.from_user if message.from_user else None
		message_owner = "owner" if user.is_self else "sudo" if user.id in client.SudoUsers() else "unknown" 

		if message_owner == "unknown":
			return False

		if not "channel" in allow:
			if message.chat.type == "channel":
				return False

		if not "forward" in allow:
			if message.forward_date:
				return False

		if not "edited" in allow:
			if message.edit_date:
				return False


		flt.prefixes = client.MyPrefix() # workaround

		for prefix in flt.prefixes:
			if not text.startswith(prefix):
				continue

			for cmd in flt.commands:
				if prefix+cmd == text.split()[0]: # split on spaces
					message.command = text.split()
					if message_owner == "sudo":
						if not client.SudoCmds(): # empty config -> full command access to sudo
							return True 

						if not cmd in client.SudoCmds():
							return False

					return True

		return False

	commands = commands if isinstance(commands, list) else [commands]
	commands = {c if case_sensitive else c.lower() for c in commands}

	prefixes = [] if prefixes is None else prefixes
	prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
	prefixes = set(prefixes) if prefixes else {""}

	return create(
		func,
		"MessageCommandFilter",
		commands=commands,
		prefixes=prefixes,
		case_sensitive=case_sensitive
	)

