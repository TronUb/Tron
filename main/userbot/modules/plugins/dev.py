""" dev plugin """

import re
import sys
import traceback
import subprocess

from io import StringIO

from pyrogram.types import Message

from main import app
from main.core.enums import UserType


@app.on_cmd(
    commands=["eval", "e"],
    usage="Run Python programs (script level). Warning: Be careful, you might delete your data.",
)
async def evaluate_handler(_, m: Message):
    """Execute Python code securely within the bot."""

    try:
        if app.command() == 1:
            return await app.send_edit(
                "Give me some Python code to execute . . .", text_type=["mono"], delme=4
            )

        # Extract the command text
        text = m.sudo_message.text if getattr(m, "sudo_message", None) else m.text
        cmd = text.split(None, 1)[1]

        msg = await app.send_edit("Executing . . .", text_type=["mono"])

        # Redirect stdout and stderr
        old_stdout, old_stderr = sys.stdout, sys.stderr
        redirected_output, redirected_error = StringIO(), StringIO()
        sys.stdout, sys.stderr = redirected_output, redirected_error

        stdout, stderr, exc = None, None, None

        try:
            await app.aexec(cmd)  # Execute the command asynchronously
        except Exception:
            exc = traceback.format_exc()

        # Capture outputs
        stdout = redirected_output.getvalue().strip()
        stderr = redirected_error.getvalue().strip()

        # Restore stdout and stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr

        # Determine final output
        evaluation = exc or stderr or stdout or "Success"
        final_output = f"**• PROGRAM:**\n\n`{cmd}`\n\n**• OUTPUT:**\n\n`{evaluation}`"

        # Handle large output
        if len(final_output) > 4096:
            await app.create_file(
                filename="eval_output.txt", content=final_output, caption=f"`{cmd}`"
            )
            await msg.delete()
        else:
            await app.send_edit(final_output)

    except Exception as e:
        await app.error(e)


@app.on_cmd(
    commands=["term", "shell"],
    usage="Execute shell scripts.",
    disable_for=UserType.SUDO
)
async def terminal_handler(_, m: Message):
    """Execute shell commands and return output."""
    try:
        if app.command() == 1:
            return await app.send_edit("Use: `.term pip3 install colorama`", delme=5)

        await app.send_edit("Running in shell . . .", text_type=["mono"])

        # Extract command text (for sudo or normal users)
        text = m.sudo_message.text if getattr(m, "sudo_message", None) else m.text
        pattern = r""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)"""

        cmd = text.split(None, 1)[1]  # Extract actual command
        output = ""

        if "\n" in cmd:  # If multi-line command
            for command in cmd.split("\n"):
                shell = [x.replace('"', "") for x in re.split(pattern, command) if x]

                try:
                    process = subprocess.Popen(
                        shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    stdout, stderr = process.communicate()
                    output += f"**{command}**\n{stdout.strip()}\n{stderr.strip()}\n"
                except Exception as e:
                    return await app.send_edit(f"**Error:**\n\n`{e}`")

        else:  # Single-line command
            shell = [x.replace('"', "") for x in re.split(pattern, cmd) if x]

            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                stdout, stderr = process.communicate()
            except Exception:
                errors = traceback.format_exc()
                return await app.send_edit(f"**Error:**\n\n`{errors}`")

            output = stdout.strip() or stderr.strip() or "No Output"

        # Handle large output
        if len(output) > 4096:
            await app.create_file(
                filename="term_output.txt", content=output, caption=f"`{cmd}`"
            )
        else:
            await app.send_edit(
                f"**COMMAND:**\n\n`{cmd}`\n\n\n**OUTPUT:**\n\n`{output}`"
            )

    except Exception as e:
        await app.error(e)
