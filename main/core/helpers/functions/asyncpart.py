import os
import math
import json
import random
import asyncio
import traceback
import datetime

from time import time
from datetime import timedelta

from typing import List, Union

from pyrogram.raw import functions
from pyrogram.raw import types
from pyrogram.errors import (
    PeerIdInvalid,
    BotMethodInvalid,
    MessageNotModified,
    FloodWait,
    YouBlockedUser
)
from pyrogram.types import (
    Message,
)
from pyrogram.enums import (
    ParseMode,
    ChatType
)

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

import aiohttp
from aiohttp.client_exceptions import ContentTypeError




class AsyncPart(object):
    @staticmethod
    async def GetRequest(link: str="", resptype: str=""):
        """ args:
                link: str = ""
                resptype: str = "json"

                Note: resptype is 'json' by default
                    available args for restype:
                    'json', 'text', 'jsontext', 'raw', 'url'
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                stored = {"json":"json", "text":"text", "jsontext":"text", "raw":"read", "url":"url"}
                try:
                    returntype = resptype if resptype and resptype in stored.keys() else stored.get("json")
                    if returntype == "jsontext":
                        return json.loads(await resp.text())
                    return await getattr(resp, returntype, None)()
                except ContentTypeError:
                    return json.loads(await resp.text())


    async def IsAdmin(self, privileges):
        """Check if we are an admin."""
        if not self.m.from_user:
            raise Exception("message is None in app.IsAdmin method")

        resp = (await self.invoke(
                functions.channels.GetParticipant(
                    channel=await self.resolve_peer(self.m.chat.id),
                    participant=await self.resolve_peer(self.id)
                )
            )
            ).participant

        if not isinstance(resp, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)):
            return False

        if resp is None:
            raise Exception("app.IsAdmin returned None")

        return True if getattr(resp.admin_rights, privileges) else False


    async def IsReply(self, msg: Message):
        """Check if the message is a reply to another user."""
        return True if msg.reply_to_message else False


    async def ProgressForPyrogram(self, current, total, ud_type, message, start):
        """ generic progress display for Telegram Upload / Download status """
        now = time()
        diff = now - start
        if round(diff % 10.00) == 0 or current == total:
            # if round(current / total * 100, 0) % 5 == 0:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = elapsed_time + time_to_completion

            elapsed_time = self.TimeFormator(milliseconds=elapsed_time)
            estimated_total_time = self.TimeFormator(milliseconds=estimated_total_time)

            progress = "**[{0}{1}]** \n**Progress**: __{2}%__\n".format(
                "".join(["●" for i in range(math.floor(percentage / 5))]),
                "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )

            tmp = progress + "**Done:** __{0} of {1}__\n**Speed:** __{2}/s__\n**ETA:** __{3}__\n".format(
                self.HumanBytes(current),
                self.HumanBytes(total),
                self.HumanBytes(speed),
                estimated_total_time if estimated_total_time != "" else "0 s",
            )
            try:
                await message.edit(f"{ud_type}\n {tmp}")
            except (MessageNotModified, FloodWait):
                pass


    async def IsThumbExists(self, file_name: str):
        " get thumbnail of file if it exists "
        thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
        if os.path.exists(thumb_image_path):
            thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
        elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
            metadata = extractMetadata(createParser(file_name))
            duration = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            # get a random TTL from the duration
            ttl = str(random.randint(0, duration - 1))

            thumb_image_path = self.GenTgThumb(file_name)
        else:
            thumb_image_path = None
        return thumb_image_path


    async def RunCommand(self, shell_command: List) -> str:
        " run shell commands "
        process = await asyncio.create_subprocess_exec(
            *shell_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        return t_response, e_response


    async def ExtractUser(self, msg: Message) -> Union[int, str]:
        """extracts the user from a message"""
        user_id = None
        first_name = None
        reply = msg.reply_to_message

        if reply:
            if reply.from_user:
                user_id = reply.from_user.id
                first_name = reply.from_user.first_name

        elif not reply:
            if msg.from_user:
                user_id = msg.from_user.id
                first_name = msg.from_user.first_name

        return user_id, first_name

    async def HasteBinPaste(self, text):
        " paste anything to pasting site "
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://www.toptal.com/developers/hastebin/documents", data=text.encode("utf-8"), timeout=3
                    ) as response:
                    key = (await response.json())["key"]
                    url = f"https://hastebin.com/raw/{key}"
                    return url if key else None
        except Exception as e:
            await self.error(e)


    async def aexec(
        self,
        code: str
        ):
        """
        params:
            1. code: str :: your written python code

        use:
            use this function to execute python codes

        ex: (async)
            await app.aexec("print('Hello, World !')")
        """
        if self.is_bot:
            raise BotMethodInvalid

        globals().update({
            "app":self,
            "bot":self.bot,
            "reply":self.m.reply_to_message,
        })
        exec(
            "async def __aexec(self, m): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
        return await locals()["__aexec"](self, self.m)


    async def error(
        self,
        e,
        edit_error: bool=True
        ):
        """
        params:
            1. error :: occured error
            2. edit_error: bool, default=True :: edits | sends error message

        usage:
            use this function at the end of try/except block

        ex: (async)
            try:
                await app.send_message(message.chat.id, "This is a test")
            except Exception as e:
                await app.error(e, edit_error=False)
        """
        if self.is_bot:
            raise BotMethodInvalid

        teks = "**Traceback Report:**\n\n"
        teks += f"**Date:** `{self.showdate()}`\n**Time:** `{self.showtime()}`\n\n"
        teks += "`This can be a error in tronuserbot, if you want you can forward this to @tronuserbot_support.`\n\n"
        teks += f"**Command:** `{self.m.text}`\n\n"
        teks += "`-`" * 30 + "\n\n"
        teks += f"**SHORT:** \n\n`{e}`\n\n"
        teks += f"**FULL:** \n\n`{traceback.format_exc()}`"

        try:
            if edit_error:
                if hasattr(e, "MESSAGE"):
                    await self.send_edit(f"`{e.MESSAGE}`")
                else:
                    await self.send_edit(e.args[0] if e.args else None)

            await self.send_message(self.LOG_CHAT, teks)
            print(e)

        except PeerIdInvalid:
            self.log.error(teks)
        except Exception as err:
            self.log.error(err)
        return True


    async def sleep(
        self,
        sec: int=0,
        delmsg=False
        ):
        """
        params:
            1. sec :: time to sleep in seconds
            2. delme, default=False :: delete the message if it is True

        use:
            this function deletes the message after sleeping for a given time,
            this function blocks the code

        ex: (async)
            await app.sleep(10, delmsg=True)
        """
        if self.is_bot:
            raise BotMethodInvalid

        msg = None
        await asyncio.sleep(sec)
        if delmsg and self.m.from_user.is_self:
            msg = await self.m.delete()
        return msg


    async def delete_message(
        self,
        sec: int=0
        ):
        """
        params:
            1. sec: int, default=0 :: time to sleep in seconds

        use:
            this function deletes a message after given time period
            this function works without blocking the entire execution

        ex: (async)
            await app.delete(10)
        """
        if self.is_bot:
            raise BotMethodInvalid

        if sec <= 600: # 10 min
            asyncio.create_task(self.sleep(sec=sec, delmsg=True))
            return True
        else:
            self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


    async def PluginData(
        self,
        modules: str
        ):
        """
        params:
            1. plug: str :: module name whose information is updated in app.CMD_HELP dict

        use:
            use this function to get information about a module

        ex: (async)
            await app.data("admin")
        """

        try:
            module_data = []
            module_data.clear()

            for x, y in zip(
                self.CMD_HELP.get(modules)[1].keys(),
                self.CMD_HELP.get(modules)[1].values()
                ):
                module_data.append(
                    f"CMD: `{self.Trigger()[0]}{x}`\nINFO: `{y}`\n\n"
                    )
            return module_data
        except Exception as e:
            self.log.error(e)
            return None


    async def send_edit(
        self,
        text: str,
        parse_mode=ParseMode.DEFAULT,
        disable_web_page_preview=False,
        delme : int=0,
        text_type: list=[],
        disable_notification: bool=False,
        reply_to_message_id: int=0,
        schedule_date: int=0,
        protect_content: bool=False,
        reply_markup=None,
        entities=None
        ):
        """
        params:
            1. text: str :: text to be edited or sent instead of editing
            2. disable_web_page_preview: bool, default=False :: web page preview will be shown if True
            3. delme: int, default=0 :: sleeps for given time and then deletes the message
            4. mono: bool, default=False :: all text format will become mono
            5. bold: bool, default=False :: all text format will become bold
            6. italic: bool, default=False :: all text format will become italic
            7. underline: bool, defau=False :: all text format will become underlined

        use:
            use this function to edit or send a message if failed to edit message

        ex: (async)
            await app.send_edit(
                "This text is sent or edited",
                disable_web_page_preview=True,
                delme=5,
                mono=True
            )
        """
        if self.is_bot:
            raise BotMethodInvalid

        try:
            try:
                msg = None

                if len(text) > 4096:
                    return await self.send_edit(
                        "Message text is too long.",
                        text_type=["mono"],
                        delme=3
                    )

                msg = await self.m.edit(
                    text=self.FormatText(text, textformat=text_type),
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                    entities=entities
                )
            except Exception as e:
                msg = await self.send_message(
                    chat_id=self.m.chat.id,
                    text=self.FormatText(text, textformat=text_type),
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    parse_mode=parse_mode,
                    reply_to_message_id=reply_to_message_id,
                    schedule_date=schedule_date,
                    protect_content=protect_content,
                    reply_markup=reply_markup,
                    entities=entities
                )
            #self.m = msg

        except Exception as e:
            await self.error(e)

        try:
            if delme > 0:
                asyncio.create_task(self.sleep(sec=delme, delmsg=True))

        except Exception as e:
            await self.error(e)

        return msg


    async def check_private(
        self
        ):
        """
        params:
            None

        use:
            use this to tell that they can't use some commands in private

        ex: (async)
            await app.private(message)
        """
        if self.is_bot:
            raise BotMethodInvalid

        if self.m.chat.type == ChatType.PRIVATE:
            await self.send_edit(
                "Please use these commands in groups.",
                text_type=["mono"],
                delme=3
            )
            return True
        return False


    async def create_file(
        self,
        filename: str,
        content: str,
        send: bool=True,
        caption: str=None
        ):
        """
        params:
            1. filename: str :: give a filename with some extension or without extension
            2. text: str :: contents which is going to be written in the file

        use:
            use this function to create files with any type of extension (.txt, .py, .java, .html, etc),
            this function also sends the created file.

        ex: (async)
            await app.create_file("sample.txt", "This file was created by app.create_file() method")
        """

        try:
            path = f"./downloads/{filename}"
            file = open(path, "w+")
            file.write(content)
            file.close()
            if send:
                await self.send_document(
                    self.m.chat.id,
                    path,
                    caption = caption if caption else f"**Uploaded By:** {self.UserMention()}"
                )
                if os.path.exists(path):
                    os.remove(path)

            else:
                return path
        except Exception as e:
            await self.error(e)


    async def kick_user(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        ban_time: int=31
        ):
        """
        params:
            1. chat_id: int :: chat id of the chat where this method is used
            2. user_id: int :: user id of the user you want to kick from chat

        use:
            use this function to kick a member from your chat

        ex: (async)
            await app.kick_user(chat_id, user_id, ban_time=120)
        """

        try:
            return await self.ban_chat_member(chat_id, user_id, datetime.datetime.now() + timedelta(seconds=ban_time))
        except Exception as e:
            await self.error(e)


    async def get_last_msg(
        self,
        chat_id
        ):
        """
        params:
            1. chat_id: int :: chat id of group or user
            2. reverse: bool, default=False :: if reverse is True you'll get the oldest message in chat

        use:
            use this function to get last message of the chat or user

        ex: (async)
            await app.get_last_msg(chat_id, reverse=True)
        """

        async for x in self.get_chat_history(chat_id, limit=1):
            return x


    async def toggle_inline(
        self,
        ):
        """
        params:
            None

        use:
            use this function to turn on | off inline mode of your bot

        ex: (async)
            await app.toggle_inline()
        """
        if self.is_bot:
            raise BotMethodInvalid

        try:
            botname = "BotFather"
            await self.send_edit("Processing command . . .", text_type=["mono"])
            await self.send_message(botname, "/mybots") # BotFather (93372553)
            await asyncio.sleep(0.50) # floodwaits

            data = await self.get_last_msg(botname)
            usernames = list(data[0].reply_markup.inline_keyboard)[0]

            unames = []
            unames.clear()

            for x in usernames:
                unames.append(x.text)

            await self.send_edit("Choosing bot . . . ", text_type=["mono"])

            if self.bot.username in unames:
                await data[0].click(self.bot.username)
            else:
                return await self.send_edit("Looks like you don't have a bot please, use your own bot.", text_type=["mono"], delme=4)

            data = await self.get_last_msg(botname)

            await self.send_edit("Pressing Bot Settings . . . ", text_type=["mono"])

            await data[0].click("Bot Settings")

            data = await self.get_last_msg(botname)

            await self.send_edit("checking whether inline mode is On or Off . . . ", text_type=["mono"])

            await data[0].click("Inline Mode")

            data = await self.get_last_msg(botname)

            # Turn on inline mode
            if "Turn on" in str(data[0]):
                await self.send_edit("Turning Inline mode on . . . ", text_type=["mono"])
                await data[0].click("Turn on")
                await self.send_edit("Inline mode is now turned On.", text_type=["mono"], delme=4)
            # Turn inline mode off
            elif "Turn inline mode off" in str(data[0]):
                await self.send_edit("Turning Inline mode Off . . .", text_type=["mono"])
                await data[0].click("Turn inline mode off")
                await self.send_edit("Inline mode is now turned Off.", text_type=["mono"], delme=4)
        except YouBlockedUser:
            await self.unblock_user(botname) # unblock & continue
            await self.toggle_inline() # keep process going
        except Exception as err:
            await self.error(err)


    async def add_users(
        self,
        user_id: Union[int, str, List[int], List[str]],
        chat_id: Union[int, str]
        ):
        """
        params:
            1. user_id: int :: list of telegram id of user
            2. chat_id :: chat id of a group or channel

        use:
            use this function to add users in a group / channel

        ex: (async)
            await app.add_users(user_id, chat_id)
        """

        try:
            done = await self.add_chat_members(chat_id, user_id)
            return True if done else False
        except Exception as e:
            self.log.error(e)


    async def user_exists(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str]
        ):
        """
        params:
            1. chat_id: int :: id of a telegram chat
            2. chat :: id of a telegram user

        use:
            use this function to check whether a user exists in a group or not

        ex: (async)
            await app.user_exists(user_id, chat_id)
        """

        async for x in self.get_chat_members(chat_id):
            if x.user.id == user_id:
                return True
        return False


    async def add_logbot(
        self
        ):
        """
        params:
            None

        use:
            use this function to add your bot if he is not in the log chat

        ex: (async)
            await app.check_bot_in_log_chat()
        """

        try:
            if self.bot:
                self.log.info("PROCESS: Checking presence of bot in log chat . . .\n")
                try:
                    if await self.user_exists(self.bot.id, self.LOG_CHAT) is False:
                        await self.add_users(self.bot.id, self.LOG_CHAT)
                        self.log.info("COMPLETED: Added bot in log chat . . .\n")
                    else:
                        self.log.info("COMPLETED: Bot is already present in log chat . . .\n")
                except PeerIdInvalid:
                    self.log.info("Peer id is invalid, Manually add bot to your log chat . . .\n")

            else:
                self.log.warning("Bot client is not available, please check (TOKEN, API_ID, API_HASH)")
        except Exception as err:
            await self.log.info(err)
