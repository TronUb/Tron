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



@app.on_message(gen(["eval", "e"], allow =["sudo"]))
async def evaluate_handler(_, m: Message):
	""" This function is made to execute python codes """

	if app.textlen(m) > 4096:
		return await send_edit(m, "Your message is too long ! only 4096 characters are allowed", text_type=["mono"], delme=4)

	global reply, chat_id, chat_type

	reply = m.reply_to_message
	chat_type = m.chat.type
	chat_id = m.chat.id
	text = m.text

	try:
		cmd = m.text.split(None, 1)[1]
	except IndexError:
		return await app.send_edit(m, "Give me some text (code) to execute . . .", text_type=["mono"], delme=4)

	msg = await app.send_edit(m, "Running . . .", text_type=["mono"])

	old_stderr = sys.stderr
	old_stdout = sys.stdout
	redirected_output = sys.stdout = StringIO()
	redirected_error = sys.stderr = StringIO()
	stdout, stderr, exc = None, None, None

	try:
		await app.aexec(msg, cmd)
	except Exception:
		exc = traceback.format_exc()

	stdout = redirected_output.getvalue()
	stderr = redirected_error.getvalue()
	sys.stdout = old_stdout
	sys.stderr = old_stderr
	evaluation = exc or stderr or stdout or "Success"
	final_output = f"**• COMMAND:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation.strip()}`"

	if len(final_output) > 4096:
		await app.create_file(message=msg, filename="eval_output.txt", content=str(final_output), caption=f"`{m.text}`")
		await msg.delete()
	else:
		await app.send_edit(msg, final_output)




@app.on_message(gen("term", allow =["sudo"]))
async def terminal_handler(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Use: `.term pip3 install colorama`", delme=5)

	elif app.textlen(m) > 4096:
		return await send_edit(m, "Your message is too long ! only 4096 characters are allowed", text_type=["mono"], delme=4)

	msg = await app.send_edit(m, "Running . . .", text_type=["mono"])
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
			return await app.send_edit(msg, """**Error:**\n```{}```""".format("".join(errors)))

		output = process.stdout.read()[:-1].decode("utf-8")
	if str(output) == "\n":
		output = None
	if output:
		if len(output) > 4096:
			await app.create_file(message=msg, filename="term_output.txt", content=output, caption=f"`{m.text}`")
		else:
			await app.send_edit(msg, f"**COMMAND:**\n\n{m.text}\n\n\n**OUTPUT:**\n\n`{output}`")
	else:
		await app.send_edit(msg, "**OUTPUT:**\n\n`No Output`")


