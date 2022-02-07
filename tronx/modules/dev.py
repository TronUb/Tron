import sys
import os
import re
import traceback
import subprocess

from io import StringIO

from pyrogram import filters
from pyrogram.types import Message

from tronx import *

from tronx.helpers import *




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







@app.on_message(gen(["eval", "e"], allow_channel=True))
async def evaluate(client, m: Message):
	""" This function is made to execute python codes """

	global reply, chat_id, chat_type

	access_list = ("SESSION", "API_ID",  "API_HASH", "session_name", "api_id", "api_hash")
	sensitive = [ f"app.{x}" for x in dir(self) if x in access_list] + [ f"self.{y}" for y in dir(self) if y in access_list] + [f"Config.{z}" for z in dir(self) if z in access_list]   
	warning = "Sorry but by evaluating this code your sensitive data will be exposed in this chat, aborting command !"
	reply = m.reply_to_message
	chat_type = m.chat.type
	chat_id = m.chat.id
	text_list = m.command
	p = print
	bot = app.bot

	if chat_type in ("supergroup", "group") and chat_id != app.LOG_CHAT:
		for x in text_list:
			if x in sensitive:
				return await send_edit(m, warning_message, mono=True, delme=4)	

	elif chat_type == "private" and chat_id != app.id:
		for y in text_list:
			if y in sensitive:
				return await send_edit(m, warning_message, mono=True, delme=4)	

	elif chat_type == "bot" and chat_id != app.bot.id:
		for z in text_list:
			if z in sensitive:
				return await send_edit(m, warning_message, mono=True, delme=4)

	try:
		cmd = m.text.split(None, 1)[1]
	except IndexError:
		return await app.send_edit(m, "Give me some code to execute . . .", mono=True, delme=3)

	await app.send_edit(m, "Running . . .", mono=True)

	reply_to_id = reply.message_id if reply else m.message_id

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
	evaluation = ""

	if exc:
		evaluation = exc
	elif stderr:
		evaluation = stderr
	elif stdout:
		evaluation = stdout
	else:
		evaluation = f"Success"

	final_output = f"**• COMMAND:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation.strip()}`"
	if len(final_output) > 4096:
		filename = "eval_output.txt"
		with open(filename, "w+", encoding="utf8") as out_file:
			out_file.write(str(final_output))
		await m.reply_document(
			document=filename,
			caption=f"`{cmd}`",
			disable_notification=True,
			reply_to_message_id=reply_to_id,
		)
		if os.path.exists(f"./{filename}"):
			os.remove(filename)
		await m.delete()
	else:
		await app.send_edit(m, final_output)




@app.on_message(gen("term", allow_channel=True))
async def terminal(_, m):
	if app.long(m) == 1:
		return await app.send_edit(m, "Use: `.term pip3 install colorama`", delme=5)

	await app.send_edit(m, "Running . . .", mono=True)
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
				print(e)
				await app.send_edit(m,
					"""
					**Error:**
					```{}```
					""".format(e)
				)
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
			with open("term_output.txt", "w+") as file:
				file.write(output)
			await app.send_document(
				m.chat.id,
				"output.txt",
				reply_to_message_id=m.message_id,
				caption="`Output file`",
			)
			if os.path.exists("./output.txt"):
				os.remove("output.txt")
		else:
			await app.send_edit(m, f"**OUTPUT:**\n\n```{output}```")
	else:
		await app.send_edit(m, "**OUTPUT:**\n\n`No Output`")


