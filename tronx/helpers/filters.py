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
from config import Config
from tronx.database.postgres.dv_sql import DVSQL 

dv = DVSQL()


# custom regex filter
def regex(
	pattern: Union[str, Pattern], 
	flags: int = 0,
	allow_sudo: bool = True,
	allow_forward: bool = False,
	allow_channel: bool = False,
	allow_edit: bool = True
	):

	async def func(flt, client: Client, update: Update):

		# works for you & sudo | only for you
		if allow_sudo:
			if update.from_user and not (update.from_user.is_self or update.from_user.id in client.SudoUsers()):
				return False
		elif not allow_sudo:
			if update.from_user and not update.from_user.is_self:
				return False

		if not allow_forward:
			if update.forward_date: 
				return False

		if not allow_channel:
			if update.chat.type == "channel": 
				return False

		if not allow_edit:
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



def MyPrefix():
	"""Multiple prefix support function"""
	return dv.getdv("PREFIX").split() or Config.PREFIX.split() or "."



# custom command filter
def gen(
	commands: Union[str, List[str]], 
	prefixes: Union[str, List[str]] = MyPrefix(), 
	case_sensitive: bool = True, 
	allow_sudo: bool = True,
	allow_forward: bool = False,
	allow_channel: bool = False,
	allow_edit: bool = True,
	):

	# update the commands and information of commands.

	# modified func of pyrogram.filters.command
	command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
	async def func(flt, client: Client, message: Message):
		# Username shared among all commands; used for mention commands, e.g.: /start@username
		global username

		username = ""

		text = message.text or message.caption
		message.command = None

		if not text:
			return False

		# works for you & sudo | only for you
		if allow_sudo:
			if message.from_user and not (message.from_user.is_self or message.from_user.id in client.SudoUsers()):
				return False
		elif not allow_sudo:
			if message.from_user and not message.from_user.is_self:
				return False

		if allow_forward is False:
			if message.forward_date:
				return False

		if allow_channel is False:
			if message.chat.type == "channel":
				return False

		if allow_edit is False:
			if message.edit_date:
				return False

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


