import os
import math
import asyncio
import traceback
import datetime
import hachoir

from functools import lru_cache

from time import time
from datetime import timedelta

from typing import List, Union, Optional, Dict, Any, Tuple

from pyrogram.raw import functions
from pyrogram.raw import types
from pyrogram.errors import (
    PeerIdInvalid,
    MessageNotModified,
    FloodWait,
    YouBlockedUser,
    MessageAuthorRequired,
    MessageIdInvalid,
)
from pyrogram.types import (
    Message,
)
from pyrogram.enums import ParseMode, ChatType

import aiohttp

# pylint: disable=no-member
class AsyncPart(object):
    @staticmethod
    async def fetch_url(
        url: str,
        method: str = "GET",
        session: Optional[aiohttp.ClientSession] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Fetch a URL asynchronously using aiohttp.

        Args:
            url (str): The URL to fetch.
            method (str): HTTP method (GET, POST, etc.). Default is "GET".
            session (aiohttp.ClientSession, optional): Reusable session. If None, creates a new one.
            **kwargs: Additional aiohttp parameters like headers, params, timeout, json, etc.

        Returns:
            Dict[str, Any]: Response dictionary with `status`, `headers`, `data`, and `error` if any.
        """

        response_data = {"status": None, "headers": {}, "data": None, "error": None}

        try:
            async with session or aiohttp.ClientSession() as s:
                async with s.request(method, url, **kwargs) as response:
                    response_data["status"] = response.status
                    response_data["headers"] = dict(response.headers)

                    # Determine response type based on content-type
                    if "application/json" in response.headers.get("Content-Type", ""):
                        response_data["data"] = await response.json()
                    else:
                        response_data["data"] = await response.text()

        except aiohttp.ClientError as e:
            response_data["error"] = f"Network error: {str(e)}"
        except Exception as e:
            response_data["error"] = f"Unexpected error: {str(e)}"

        return response_data

    async def is_admin(
        self, chat_id: Union[int, str], user_id: Union[int, str], privilege: str = None
    ) -> bool:
        """
        Check if a user is an admin in a chat.

        Args:
            chat_id (int | str): The chat ID.
            user_id (int | str): The user ID.
            privilege (str, optional): The admin privilege to check (e.g., "ban_users", "pin_messages").

        Returns:
            bool: True if the user has the specified privilege, False otherwise.
        """

        try:
            member = await self.get_chat_member(chat_id, user_id)

            if not member.privileges:
                return False  # User is not an admin

            if privilege:
                return getattr(member.privileges, privilege, False)

            return True  # User is an admin

        except Exception as e:
            print("e::", e)
            return False  # If an error occurs, assume not an admin

    async def is_reply(self, message: Message) -> bool:
        """
        Check if the message is a reply to another user.

        Args:
            message (Message): The message object.

        Returns:
            bool: True if the message is a reply, False otherwise.
        """
        return bool(message and message.reply_to_message)

    async def progress_for_pyrogram(self, current, total, ud_type, message, start):
        """Generic progress display for Telegram Upload / Download status"""
        now = time()
        diff = now - start

        if round(diff % 10.00) == 0 or current == total:
            percentage = current * 100 / total
            speed = current / diff if diff > 0 else 0
            elapsed_time = round(diff) * 1000
            time_to_completion = (
                round((total - current) / speed) * 1000 if speed > 0 else 0
            )
            estimated_total_time = elapsed_time + time_to_completion

            elapsed_time = self.TimeFormator(milliseconds=elapsed_time)
            estimated_total_time = self.TimeFormator(milliseconds=estimated_total_time)

            # Generate progress bar
            filled = math.floor(percentage / 5)
            empty = 20 - filled
            progress_bar = "**[{0}{1}]**".format(
                "".join(["●" for _ in range(filled)]),
                "".join(["○" for _ in range(empty)]),
            )

            # Final message text
            progress_text = (
                f"{progress_bar} \n"
                f"**Progress:** __{round(percentage, 2)}%__\n"
                f"**Done:** __{self.HumanBytes(current)} of {self.HumanBytes(total)}__\n"
                f"**Speed:** __{self.HumanBytes(speed)}/s__\n"
                f"**ETA:** __{estimated_total_time if estimated_total_time else '0 s'}__\n"
            )

            try:
                await message.edit(f"{ud_type}\n {progress_text}")
            except (MessageNotModified, FloodWait):
                pass

    async def get_file_thumbnail(self, file_name: str):
        """Get thumbnail of file if it exists."""

        thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")

        # Check if a default thumbnail exists
        if os.path.exists(thumb_image_path):
            return thumb_image_path

        # If no default thumbnail, generate one for video files
        if file_name and file_name.lower().endswith(("mp4", "mkv", "webm")):
            parser = hachoir.parser.createParser(file_name)

            if parser:
                metadata = hachoir.metadata.extractMetadata(parser)

                if metadata and metadata.has("duration"):
                    duration = metadata.get("duration").seconds  # If needed later

            # Generate thumbnail
            generated_thumb = self.GenTgThumb(file_name)

            if generated_thumb and os.path.exists(generated_thumb):
                return generated_thumb

        return None  # No thumbnail found

    async def run_in_shell(self, shell_command: List[str]) -> Tuple[str, str]:
        """Runs a shell command asynchronously.

        Args:
            shell_command (List[str]): The shell command as a list of arguments.

        Returns:
            Tuple[str, str]: Standard output and error output.
        """

        if not shell_command:
            return "", "Error: No command provided"

        try:
            process = await asyncio.create_subprocess_exec(
                *shell_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            return stdout.decode().strip(), stderr.decode().strip()

        except Exception as e:
            return "", f"Error executing command: {str(e)}"

    async def paste_to_bin(self, text: str) -> str:
        """Paste text to 0x0.st and return the paste URL."""

        if not text:
            return "Error: No text provided for pasting."

        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.post(
                    "https://0x0.st", data={"file": text.encode("utf-8")}
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    return f"Error: Failed to paste. HTTP {response.status}"

        except Exception as e:
            await self.error(f"paste_to_bin Error: {str(e)}")
            return "Error: Something went wrong while pasting."

    async def async_exec(self, message, python_code: str):
        """
        Execute Python code asynchronously.

        Args:
            message (Message): The message object (for context).
            python_code (str): The Python code to execute.

        Usage:
            await app.async_exec(message, "print('Hello, World!')")
        """

        exec_namespace = {
            "app": self,
            "bot": getattr(self, "bot", None),
            "reply": message.reply_to_message,
            "asyncio": asyncio,  # Enables async operations in execution
        }

        try:
            # Define and execute an async function dynamically
            exec(
                "async def _exec_func():\n"
                + "\n".join(f"    {line}" for line in python_code.split("\n")),
                exec_namespace,
            )
            return await exec_namespace["_exec_func"]()

        except Exception as error:
            return f"Error executing code: {str(error)}"

    async def log_error(self, error: Exception, message=None, edit_error: bool = True):
        """
        Log and handle errors in the bot.

        Args:
            error (Exception): The occurred exception.
            message (Message, optional): The message object (if available).
            edit_error (bool, optional): Whether to edit the error message in the chat. Defaults to True.

        Usage:
            try:
                await app.send_message(message.chat.id, "Test message")
            except Exception as e:
                await app.log_error(e, message)
        """

        # Generate full traceback
        full_traceback = traceback.format_exc()

        # If running as a bot, just log the error
        if self.is_bot:
            print(full_traceback)
            return

        # Prepare error report
        error_report = "**Traceback Report:**\n\n"
        error_report += f"**Date:** `{self.get_date()}`\n"
        error_report += f"**Time:** `{self.get_time()}`\n\n"

        if message:
            error_report += (
                f"**Chat Name:** `{message.chat.first_name or message.chat.title}`\n"
            )
            error_report += f"**Chat Type:** `{message.chat.type.value}`\n"
            error_report += f"**Message Owner:** `{message.from_user.type.value}`\n\n"
            error_report += "`This might be an error in tronuserbot. Forward this to` @tronUbSupport if needed.\n\n"
            error_report += f"**Message:** `{message.text}`\n\n"

        error_report += "`-`" * 30 + "\n\n"
        error_report += f"**SHORT:** \n\n`{str(error)}`\n\n"
        error_report += f"**FULL:** \n\n`{full_traceback}`"

        try:
            # Edit error message in chat if needed
            if edit_error:
                await self.send_edit(message=message, text=f"`{str(error)}`")

            # Send full error log
            if len(error_report) > 4096:
                await self.create_file(
                    message=message, filename="exception.txt", content=error_report
                )
            else:
                await self.send_message(self.LogChat, error_report)

            print(full_traceback)

        except PeerIdInvalid:
            self.log.error("Invalid LogChat ID. Cannot send error report.")
        except Exception as log_error:
            self.log.error(f"Error while logging error: {log_error}")

        return True

    async def delete_after_sleep(
        self, message: Message, seconds: int = 0, delete_after: bool = False
    ):
        """
        Sleep for a given time and optionally delete a message.

        Args:
            message (Message): The message object to delete.
            seconds (int): Time to wait before deletion (default is 0).
            delete_after (bool): Whether to delete the message after sleeping (default is False).

        Example:
            await app.sleep_delete(message, 10, delete_after=True)
        """

        if self.is_bot:
            raise RuntimeError("This function cannot be used in bot mode.")

        if not message:
            return None  # No message provided, nothing to do.

        await asyncio.sleep(seconds)

        if delete_after:
            return await message.delete()

        return None

    async def delete_message(self, message: Message, delay: int = 0):
        """
        Deletes a message after a given time period without blocking execution.

        Args:
            message (Message): The message to delete.
            delay (int, optional): Time to wait before deletion (in seconds). Defaults to 0.

        Returns:
            bool: True if deletion was scheduled, False otherwise.

        Example:
            await app.delete_message(message, 10)
        """

        if self.is_bot:
            raise RuntimeError("This function cannot be used in bot mode.")

        if delay > 600:
            self.log.error(
                "Delete function can only delay for up to 10 minutes (600 sec)."
            )
            return False

        # Schedule deletion without blocking execution
        async def delayed_delete():
            await asyncio.sleep(delay)
            await message.delete()

        asyncio.create_task(delayed_delete())

        return True

    async def get_plugin_info(self, module_name: str):
        """
        Get information about a module.

        Args:
            module_name (str): The name of the module to fetch information for.

        Returns:
            list[str] | None: A list of formatted command info or None if the module is not found.

        Example:
            await app.get_plugin_info("admin")
        """

        try:
            # Fetch module data or return None if not found
            commands = self.CMD_HELP.get(module_name, {})

            if not commands:
                return None  # No data found

            # Format command usage info
            command_info = [
                f"**CMD:** `{self.Trigger[0]}{cmd}`\n**INFO:** `{usage}`\n\n"
                for cmd, usage in commands.items()
            ]

            return command_info

        except Exception as error:
            self.log.error(f"Error in get_plugin_info: {traceback.format_exc()}")
            return None

    async def send_edit(
        self,
        message: Message,
        text: str,
        parse_mode=ParseMode.DEFAULT,
        disable_web_page_preview=False,
        delete_after: int = 0,
        text_format: list = None,
        disable_notification: bool = False,
        reply_to_message_id: int = 0,
        schedule_date: int = 0,
        protect_content: bool = False,
        reply_markup=None,
        entities=None,
        send_as_file: bool = False,
        filename: str = None,
    ):
        """
        Edit an existing message or send a new one if editing fails.

        Args:
            message (Message): The message object to edit.
            text (str): The text to edit or send.
            parse_mode (ParseMode, optional): The parse mode for formatting.
            disable_web_page_preview (bool, optional): Disable webpage previews.
            delete_after (int, optional): Delete message after X seconds.
            send_as_file (bool, optional): Send as a file if text is too long.
            filename (str, optional): Filename when sending as file.

        Returns:
            Message: The edited or newly sent message.

        Example:
            await app.send_edit(message, "This text will be edited.", delete_after=5)
        """

        if self.is_bot:
            raise RuntimeError("This function cannot be used in bot mode.")

        try:
            result = None
            filename = filename or "file.txt"

            # Send as file if text is too long
            if len(text) > 4096 or send_as_file:
                await self.send_message(
                    message.chat.id, "Message text is too long, sending as a file."
                )
                return await self.create_file(
                    message=message, filename=filename, content=text
                )

            # Try editing the existing message
            try:
                result = await message.edit(
                    text=self.FormatText(text, textformat=text_format or []),
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                    entities=entities,
                )
            except MessageNotModified:
                pass

            except (MessageAuthorRequired, MessageIdInvalid):
                print(traceback.format_exc())

                # If editing fails, send a new message
                result = await self.send_message(
                    chat_id=message.chat.id,
                    text=self.FormatText(text, textformat=text_format or []),
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    parse_mode=parse_mode,
                    reply_to_message_id=reply_to_message_id,
                    schedule_date=schedule_date,
                    protect_content=protect_content,
                    reply_markup=reply_markup,
                    entities=entities,
                )

            # Schedule message deletion
            if delete_after > 0:
                asyncio.create_task(
                    self.delete_after_sleep(
                        message=result, seconds=delete_after, delete_after=True
                    )
                )

            return result

        except Exception as e:
            await self.log_error(e)

    async def is_command_used_in_private(self, message: Message) -> bool:
        """
        Check if a command is being used in a private chat.

        Args:
            message (Message): The message object.

        Returns:
            bool: True if used in private, False otherwise.

        Example:
            if await app.is_command_used_in_private(message):
                return  # Stop execution if in private chat
        """

        if self.is_bot:
            raise RuntimeError("This function cannot be used in bot mode.")

        if message.chat.type == ChatType.PRIVATE:
            await self.send_edit(
                message=message,
                text="Please use these commands in groups.",
                text_format=["mono"],
                delete_after=3,
            )
            return True  # Command shouldn't proceed in private chat

        return False  # Safe to use the command

    async def create_file(
        self,
        message: Message,
        filename: str,
        content: str,
        send: bool = True,
        caption: str = None,
    ):
        """
        Create a file with specified content and optionally send it.

        Args:
            message (Message): The message object to get chat info.
            filename (str): The filename (with or without extension).
            content (str): The text to write inside the file.
            send (bool, optional): Whether to send the file after creation (default: True).
            caption (str, optional): Caption for the sent file.

        Returns:
            str | bool: File path if `send=False`, else `True` after sending.

        Example:
            await app.create_file(message, "sample.txt", "This file was created by app.create_file()")
        """

        try:
            if not filename:
                return None  # No filename provided

            # Ensure the "downloads" directory exists
            os.makedirs("downloads", exist_ok=True)

            # Generate a safe file path
            base_path = os.path.join("downloads", filename)
            path = base_path
            counter = 1

            while os.path.exists(path):  # Prevent overwriting existing files
                path = (
                    f"{base_path.rsplit('.', 1)[0]}_{counter}.{filename.split('.')[-1]}"
                )
                counter += 1

            # Write content to the file
            with open(path, "w+", encoding="utf-8") as file:
                file.write(content)

            # Send the file if required
            if send:
                await self.send_document(
                    message.chat.id,
                    path,
                    caption=caption or f"**Uploaded By:** {self.UserMention}",
                )
                os.remove(path)  # Remove file after sending
                return True

            return path  # Return file path if not sending

        except Exception as error:
            await self.log_error(error)
            return None

    async def kick_user(
        self, chat_id: Union[str, int], user_id: Union[str, int], ban_time: int = 40
    ):
        """
        Kick (noban) a user from chat.

        Args:
            chat_id (Union[str, int]): The chat ID.
            user_id (Union[str, int]): The user ID.
            ban_time (int, optional): Duration in seconds before the user can rejoin. Default is 40 sec.

        Returns:
            bool: True if kicked successfully, False if an error occurs.

        Example:
            await app.kick_user(chat_id, user_id, ban_time=120)
        """

        try:
            ban_time = max(ban_time, 1)  # Ensure positive ban time
            unban_date = datetime.datetime.now() + timedelta(seconds=ban_time)
            return await self.ban_chat_member(chat_id, user_id, until_date=unban_date)

        except Exception as error:
            await self.log_error(error, None)
            return False

    async def get_lastmessage(
        self, chat_id: Union[int, str], reverse: bool = False
    ) -> Optional[Message]:
        """
        Get the first or last message of a chat.

        Args:
            chat_id (Union[int, str]): The chat ID.
            reverse (bool, optional): If True, returns the first message instead of the last.

        Returns:
            Optional[Message]: The retrieved message, or None if not found.

        Example:
            last_msg = await app.get_lastmessage(chat_id, reverse=True)
        """

        try:
            messages = await self.get_chat_history(chat_id, limit=1).flatten()

            if not messages:
                return None  # No messages found

            return messages[-1] if reverse else messages[0]

        except Exception as error:
            await self.log_error(error, None)
            return None

    async def toggle_inline(self, message):
        """
        Toggle the inline mode of your bot (On/Off).

        Returns:
            None

        Example:
            await app.toggle_inline()
        """

        if self.is_bot:
            raise RuntimeError("This function cannot be used in bot mode.")

        BOTFATHER = "BotFather"

        try:
            await self.send_edit(
                message=message, text="Processing command...", text_format=["mono"]
            )
            await self.send_message(BOTFATHER, "/mybots")
            await asyncio.sleep(0.5)  # Avoid floodwaits

            data = await self.get_last_msg(BOTFATHER)

            if not data:
                return await self.send_edit(
                    message=message,
                    text="Failed to retrieve bot list.",
                    text_format=["mono"],
                    delete_after=4,
                )

            # Extract bot usernames
            bot_usernames = [
                btn.text for btn in data[0].reply_markup.inline_keyboard[0]
            ]

            await self.send_edit(
                message=message, text="Choosing bot...", text_format=["mono"]
            )

            if self.bot.username in bot_usernames:
                await data[0].click(self.bot.username)
            else:
                return await self.send_edit(
                    message=message,
                    text="You don't have a bot or are using the wrong bot. Please use your own bot.",
                    text_format=["mono"],
                    delete_after=4,
                )

            # Navigate to Bot Settings
            data = await self.get_last_msg(BOTFATHER)
            await self.send_edit(
                message=message, text="Accessing Bot Settings...", text_format=["mono"]
            )
            await data[0].click("Bot Settings")

            # Navigate to Inline Mode settings
            data = await self.get_last_msg(BOTFATHER)
            await self.send_edit(
                message=message,
                text="Checking inline mode status...",
                text_format=["mono"],
            )
            await data[0].click("Inline Mode")

            data = await self.get_last_msg(BOTFATHER)

            # Toggle inline mode
            if "Turn on" in str(data[0]):
                await self.send_edit(
                    message=message,
                    text="Turning inline mode on...",
                    text_format=["mono"],
                )
                await data[0].click("Turn on")
                await self.send_edit(
                    message=message,
                    text="Inline mode is now **On**.",
                    text_format=["mono"],
                    delete_after=4,
                )
            elif "Turn inline mode off" in str(data[0]):
                await self.send_edit(
                    message=message,
                    text="Turning inline mode off...",
                    text_format=["mono"],
                )
                await data[0].click("Turn inline mode off")
                await self.send_edit(
                    message=message,
                    text="Inline mode is now **Off**.",
                    text_format=["mono"],
                    delete_after=4,
                )

        except YouBlockedUser:
            await self.unblock_user(BOTFATHER)  # Unblock and retry
            await self.toggle_inline(message=message)  # Continue process

        except Exception as error:
            await self.log_error(error, None)

    async def add_users(
        self, chat_id: Union[int, str], user_id: Union[int, str, List[int], List[str]]
    ):
        """
        Add users to a group or supergroup.

        Args:
            chat_id (Union[int, str]): The chat ID where users should be added.
            user_id (Union[int, str, List[int], List[str]]): The user(s) to add.

        Returns:
            bool: True if successful, False if an error occurs.

        Example:
            await app.add_users(chat_id, user_id)
        """

        try:
            # Ensure user_id is always a list
            if isinstance(user_id, (int, str)):
                user_id = [user_id]  # Convert single user to list

            return await self.add_chat_members(chat_id, user_id)

        except Exception as error:
            await self.log_error(error, None)
            return False

    async def is_user_in_group(
        self, chat_id: Union[int, str], user_id: Union[int, str]
    ) -> bool:
        """
        Check if a user is in a group or not.

        Args:
            chat_id (Union[int, str]): The chat ID to check.
            user_id (Union[int, str]): The user ID to check.

        Returns:
            bool: True if user is in group, False otherwise.

        Example:
            if await app.user_ingroup(chat_id, user_id):
                print("User is in the group.")
        """

        try:
            member = await self.get_chat_member(chat_id, user_id)
            return member is not None  # If the user exists, return True

        except Exception as error:
            await self.log_error(error, None)
            return False  # User is not in group or an error occurred

    async def add_assistant_in_logchat(self) -> bool:
        """
        Add the assistant bot to the log chat.

        Returns:
            bool: True if the bot was added successfully, False if it was already in the group or an error occurred.

        Example:
            success = await app.add_assistant_in_logchat()
            if success:
                print("Bot added to log chat!")
        """

        try:
            if not self.bot:
                await self.log_error("Bot client is not available.", None)
                return False  # Bot is not initialized

            if await self.user_ingroup(self.LogChat, self.bot.id):
                await self.log_error("Bot is already in the log group.", None)
                return False  # Bot is already in the group

            return await self.add_users(
                self.LogChat, self.bot.id
            )  # Add bot to log chat

        except Exception as error:
            await self.log_error(error, None)
            return False

    async def send_start_message(self) -> bool:
        """
        Send a start message to the bot's owner.

        Returns:
            bool: True if the message was sent successfully, False otherwise.

        Example:
            success = await app.send_start_message()
            if success:
                print("Start message sent!")
        """

        try:
            if not self.bot:
                await self.log_error("Bot instance is not available.", None)
                return False  # Bot is not initialized

            # Ensure the bot can interact with the user
            await self.get_chat(self.UserId)

            await self.bot.send_message(
                self.UserId,
                "The userbot is online now.",
                reply_markup=self.buildMarkup(
                    [self.buildButton(text="Support Group", url="t.me/tronubsupport")]
                ),
            )

            return True  # Message sent successfully

        except Exception as error:
            await self.log_error(error, None)
            return False

    async def mute_notification(
        self,
        chat_id: Union[str, int],
        show_previews: bool = None,
        silent: bool = True,
        mute_until: int = None,
        sound: types.NotificationSound = None,
    ) -> bool:
        """
        Mute notifications for a chat.

        Args:
            chat_id (Union[str, int]): The chat ID.
            show_previews (bool, optional): Whether to show message previews.
            silent (bool, optional): Whether to mute the chat silently.
            mute_until (int, optional): Timestamp until when the chat should be muted.
            sound (NotificationSound, optional): Custom notification sound.

        Returns:
            bool: True if successful, False otherwise.

        Example:
            success = await app.mute_notification(chat_id, mute_until=3600)
            if success:
                print("Chat muted!")
        """

        try:
            peer = await self.resolve_peer(chat_id)

            # Ensure mute_until is a valid timestamp
            mute_until = max(mute_until or int(time.time()) + 3600, int(time.time()))

            await self.invoke(
                functions.UpdateNotifySettings(
                    peer=types.InputNotifyPeer(peer=peer),
                    settings=functions.InputPeerNotifySettings(
                        show_previews=show_previews,
                        silent=silent,
                        mute_until=mute_until,
                        sound=sound,
                    ),
                )
            )

            return True  # Mute applied successfully

        except Exception as error:
            await self.log_error(error, None)
            return False  # Mute failed

    async def unmute_notification(self, chat_id: Union[str, int]) -> bool:
        """
        Unmute notifications for a chat.

        Args:
            chat_id (Union[str, int]): The chat ID.

        Returns:
            bool: True if successful, False otherwise.

        Example:
            success = await app.unmute_notification(chat_id)
            if success:
                print("Chat unmuted!")
        """

        try:
            return await self.mute_notification(
                chat_id=chat_id,
                show_previews=True,
                silent=False,
                mute_until=None,
                sound=None,
            )

        except Exception as error:
            await self.log_error(error, None)
            return False  # Unmute failed

    @lru_cache(maxsize=100)
    async def get_anime_details_jikan(
        self, anime_name: Optional[str] = None, mal_id: Optional[int] = None
    ):
        """Fetch anime details and characters from Jikan API."""
        if not anime_name and not mal_id:
            return {
                "success": False,
                "error": "Either anime_name or mal_id must be provided.",
            }

        base_url = "https://api.jikan.moe/v4/anime"
        if mal_id:
            # Fetch anime details directly using mal_id
            base_url = f"https://api.jikan.moe/v4/anime/{mal_id}"
        else:
            # Search for anime by name
            base_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"

        try:
            # Fetch anime details and characters concurrently
            anime_data, characters = await asyncio.gather(
                self._fetch_anime_data(base_url),
                self._fetch_characters(mal_id) if mal_id else asyncio.sleep(0),
            )

            if not anime_data:
                return {"success": False, "error": "No anime found."}

            anime_details = self._parse_anime_details(anime_data)
            return {
                "success": True,
                "anime_details": anime_details,
                "characters": characters if characters else [],
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _fetch_anime_data(self, url: str) -> Optional[Dict]:
        """Fetch anime data from the Jikan API."""
        try:
            response = await self.fetch_url(url)
            if response.status == 200:
                data = await response.json()
                return (
                    data.get("data", [{}])[0]
                    if "data" in data
                    else data.get("data", {})
                )
            return None
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None

    async def _fetch_characters(self, mal_id: int) -> Optional[List[Dict]]:
        """Fetch anime characters from the Jikan API."""
        try:
            char_url = f"https://api.jikan.moe/v4/anime/{mal_id}/characters"
            response = await self.fetch_url(char_url)
            if response.status == 200:
                char_data = await response.json()
                return [
                    {
                        "name": char["character"]["name"],
                        "mal_url": char["character"]["url"],
                        "role": char.get("role", "Unknown"),
                    }
                    for char in char_data.get("data", [])
                ]
            return None
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None

    def _parse_anime_details(self, anime: Dict) -> Dict:
        """Parse anime details from the API response."""
        return {
            "title": anime.get("title_english", anime.get("title", "Unknown")),
            "japanese_title": anime.get("title_japanese", "N/A"),
            "synonyms": anime.get("title_synonyms", []),
            "mal_url": anime.get("url", "N/A"),
            "image": anime.get("images", {}).get("jpg", {}).get("image_url", "N/A"),
            "trailer": anime.get("trailer", {}).get("url", "N/A"),
            "episodes": anime.get("episodes", "Unknown"),
            "score": anime.get("score", "N/A"),
            "rank": anime.get("rank", "N/A"),
            "popularity": anime.get("popularity", "N/A"),
            "status": anime.get("status", "N/A"),
            "source": anime.get("source", "N/A"),
            "genres": [genre["name"] for genre in anime.get("genres", [])],
            "themes": [theme["name"] for theme in anime.get("themes", [])],
            "demographics": [demo["name"] for demo in anime.get("demographics", [])],
            "synopsis": anime.get("synopsis", "No synopsis available."),
            "aired": anime.get("aired", {}).get("string", "N/A"),
            "duration": anime.get("duration", "N/A"),
            "rating": anime.get("rating", "N/A"),
            "favorites": anime.get("favorites", 0),
            "mal_id": anime.get("mal_id"),
        }
