import os
import re

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

	# update the commands and information of commands.

	# modified func of pyrogram.filters.command
	command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
	async def func(flt, client: Client, message: Message):
		# Username shared among all commands; used for mention commands, e.g.: /start@username
		global username, raw_commands

		username = ""

		text = message.text or message.caption
		message.command = None
		is_owner = message.from_user.is_self
		is_sudo = True if message.from_user.id in client.SudoUsers() else False

		if not text:
			return False

		if not is_owner:
			return False
		elif not is_sudo:
			return False


		flt.prefixes = client.MyPrefix() # workaround

		for prefix in flt.prefixes:
			if not text.startswith(prefix):
				continue

			without_prefix = text[len(prefix):]

			username = None

			for cmd in flt.commands:
				if not re.match(rf"^(?:{cmd}(?:@?{username})?)(?:\s|$)", without_prefix,
					flags=re.IGNORECASE if not flt.case_sensitive else 0):
					continue

				without_command = re.sub(rf"{cmd}(?:@?{username})?\s?", "", without_prefix, count=1)

				message.command = [cmd] + [
					re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
					for m in command_re.finditer(without_command)
				]
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

