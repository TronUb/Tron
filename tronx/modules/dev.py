import sys
import os
import re
import traceback
import subprocess

from io import StringIO

from pyrogram import filters

from tronx import (
	app, 
	CMD_HELP,
)

from tronx.helpers import (
	error,
	gen,
	send_edit,
	long,
)




CMD_HELP.update(
	{"dev" : (
		"dev",
		{
		"eval print('cat')" : "A nice tool to test python codes.",
		"term pip3 install pyrogram" : "Run commands in shell."
		}
		)
	}
)




async def aexec(code, app, m):
	exec(
		f"async def __aexec(app, m): "
		+ "".join(f"\n {l}" for l in code.split("\n"))
	)
	return await locals()["__aexec"](app, m)




@app.on_message(gen(["eval", "e"]))
async def evaluate(app, m):
	try:
		cmd = m.text.split(" ", maxsplit=1)[1]
	except IndexError:
		await send_edit(
			m, 
			"Give me some code to execute ..."
			)
		return
	await send_edit(m, "`Running ...`")
	reply_to_id = m.message_id
	if m.reply_to_message:
		reply_to_id = m.reply_to_message.message_id
	old_stderr = sys.stderr
	old_stdout = sys.stdout
	redirected_output = sys.stdout = StringIO()
	redirected_error = sys.stderr = StringIO()
	stdout, stderr, exc = None, None, None
	try:
		await aexec(cmd, app, m)
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
		os.remove(filename)
		await m.delete()
	else:
		await send_edit(
			m,
			final_output
			)




@app.on_message(gen("term"))
async def terminal(app, m):
	if len(m.text.split()) == 1:
		await send_edit(m, "Use: `.term pip3 install pyrogram`")
		return
	await send_edit(m, "`Running ...`")
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
				await send_edit(m,
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
			await send_edit(m, """**Error:**\n```{}```""".format("".join(errors)))
			return
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
			os.remove("output.txt")
			return
		await send_edit(m, f"**Output:**\n```{output}```")
	else:
		await send_edit(m, "**Output:**\n`No Output`")




@app.on_message(gen("py"))
async def py_helper(_, m: Message):
	try:
		if long(m) == 1:
			await send_edit(m, "Please give me some input after command . . .")
		elif long(m) > 1 and long(m) < 4096:
			text = m.text.split(None, 1)[1]
			await send_edit(m, f"Getting py info for {text}")
			search = help(text)
			if search:
				await send_edit(m, search)
			else:
				await send_edit(m, "No results found !")
		elif long(m) > 4096:
			await send_edit(m, "maximum input characters 4096 . . .")
			
	except Exception as e:
		await error(m, e)