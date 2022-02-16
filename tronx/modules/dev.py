import sys
import os
import re
import traceback
import subprocess

from io import StringIO

from pyrogram import filters
from pyrogram.types import Message

from tronx import app
from tronx.helpers import gen




app.CMD_HELP.update(
	{"dev" : (
		"dev",
		{
		"eval print('cat')" : "A nice tool to test python codes.",
		"term pip3 install colorama" : "Run commands in shell."
		}
		)
	}
)




bot = app.bot
p = print



@app.on_message(gen(["eval", "e"], allow_channel=True))
async def evaluate(app, m: Message):
	""" This function is made to execute python codes """

	if app.textlen(m) > 4096:
		return await send_edit(m, "Your message is too long ! only 4096 characters are allowed", mono=True, delme=4)

	global reply, chat_id, chat_type, p, bot

	access_list = ("SESSION", "API_ID",  "API_HASH", "session_name", "api_id", "api_hash")
	sensitive = [ f"app.{x}" for x in dir(app) if x in access_list] + [ f"self.{y}" for y in dir(app) if y in access_list] + [f"Config.{z}" for z in dir(app) if z in access_list]   
	warning_message = "Sorry but by evaluating this code your sensitive data will be exposed in this chat, aborting command !"
	reply = m.reply_to_message
	chat_type = m.chat.type
	chat_id = m.chat.id
	text = m.text

	if chat_type in ("supergroup", "group") and chat_id != app.LOG_CHAT:
		for x in sensitive:
			if x in text:
				return await app.send_edit(m, warning_message, mono=True, delme=4)	

	elif chat_type == "private" and chat_id != app.id:
		for y in sensitive:
			if y in text:
				return await app.send_edit(m, warning_message, mono=True, delme=4)	

	elif chat_type == "bot" and chat_id != app.bot.id:
		for z in sensitive:
			if z in text:
				return await app.send_edit(m, warning_message, mono=True, delme=4)

	try:
		cmd = m.text.split(None, 1)[1]
	except IndexError:
		return await app.send_edit(m, "Give me some text (code) to execute . . .", mono=True, delme=3)

	m = await app.send_edit(m, "Running . . .", mono=True)

	old_stderr = sys.stderr
	old_stdout = sys.stdout
	redirected_output = sys.stdout = StringIO()
	redirected_error = sys.stderr = StringIO()
	stdout, stderr, exc = None, None, None

	try:
		await app.aexec(m, cmd)
	except Exception:
		exc = traceback.format_exc()

	stdout = redirected_output.getvalue()
	stderr = redirected_error.getvalue()
	sys.stdout = old_stdout
	sys.stderr = old_stderr
	evaluation = exc or stderr or stdout or "Success"
	final_output = f"**• COMMAND:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation.strip()}`"

	if len(final_output) > 4096:
		await app.create_file(m, "eval_output.txt", str(final_output))
		await m.delete()
	else:
		await app.send_edit(m, final_output)




@app.on_message(gen("term", allow_channel=True))
async def terminal(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Use: `.term pip3 install colorama`", delme=5)

	elif app.textlen(m) > 4096:
		return await send_edit(m, "Your message is too long ! only 4096 characters are allowed", mono=True, delme=4)

	m = await app.send_edit(m, "Running . . .", mono=True)
	args = m.text.split(None, 1)
	teks = args[1]
	if "\n" in teks:
		code = teks.split("\n")
		output = ""
		for x in code:
			shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
			try:
				process = subprocess.Popen(
					shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
				)
			except Exception as e:
				await app.error(m, e)
			output += "**{}**\n".format(code)
			output += process.stdout.read()[:-1].decode("utf-8")
			output += "\n"
	else:
		shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
		for a in range(len(shell)):
			shell[a] = shell[a].replace('"', "")
		try:
			process = subprocess.Popen(
				shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
			)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			errors = traceback.format_exception(
				etype=exc_type, value=exc_obj, tb=exc_tb
			)
			return await app.send_edit(m, """**Error:**\n```{}```""".format("".join(errors)))

		output = process.stdout.read()[:-1].decode("utf-8")
	if str(output) == "\n":
		output = None
	if output:
		if len(output) > 4096:
			await app.create_file(m, "term_output.txt", output)
		else:
			await app.send_edit(m, f"**OUTPUT:**\n\n```{output}```")
	else:
		await app.send_edit(m, "**OUTPUT:**\n\n`No Output`")


