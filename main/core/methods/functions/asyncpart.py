import os
import math
import json
import random
import asyncio
import inspect
import traceback
import datetime
import pyrogram
import hachoir

from time import time
from datetime import timedelta

from typing import (
  List,
  Union
)

from pyrogram.raw import functions
from pyrogram.raw import types
from pyrogram.errors import (
    PeerIdInvalid,
    BotMethodInvalid,
    MessageNotModified,
    FloodWait,
    YouBlockedUser,
    MessageAuthorRequired,
    MessageIdInvalid
)
from pyrogram.types import (
    Message,
)
from pyrogram.enums import (
    ParseMode,
    ChatType
)

import aiohttp
from aiohttp.client_exceptions import ContentTypeError




def messageobject(anydict: dict):
    message = None
    all_messages = [
        x for x in anydict.values()
        if isinstance(x, Message)
    ]
    try:
        # the passed message object
        # must be at the top 
        return all_messages[0]
    except IndexError:
        return None


class AsyncPart(object):
    @staticmethod
    async def GetRequest(url: str, resptype: str=""):
        """ args:
                link: str = ""
                resptype: str = "json"

                Note: resptype is 'json' by default
                    available args for restype:
                    'json', 'text', 'jsontext', 'raw', 'url'
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                stored = {
                    "json":"json",
                    "text":"text",
                    "jsontext":"text",
                    "raw":"read",
                    "url":"url"
                }
                try:
                    returntype = resptype if resptype and resptype in stored.keys() else stored.get("json")
                    if returntype == "jsontext":
                        return json.loads(await resp.text())
                    return await getattr(resp, returntype, None)()
                except ContentTypeError:
                    return json.loads(await resp.text())


    @staticmethod
    async def PostRequest(endpoint: str, payload: dict, timeout: int=3, resptype: str=""):
        """ args:
                link: str = ""
                resptype: str = "json"

                Note: resptype is 'json' by default
                    available args for restype:
                    'json', 'text', 'jsontext', 'raw', 'url'
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                data=payload,
                timeout=timeout
            ) as response:
                return (await response.json())


    async def IsAdmin(
        self,
        privileges: types.ChatAdminRights = None,
        chat_id: Union[str, int] = None,
        user_id: Union[str, int] = None
        ):
        """
        Check if you/user are an admin in chat.
        
        params::
            privileges: "raw.types.ChatAdminRights"
            chat_id: Union[str, int] = None
            user_id: Union[str, int] = None

        privileges::
            1. change_info
            2. post_messages
            3. edit_messages
            4. delete_messages
            5. ban_users
            6. invite_users
            7. pin_messages
            8. add_admins
            9. anonymous
            10. manage_call
            11. other
        """
        
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)

        r = (await self.invoke(
                functions.channels.GetParticipant(
                    channel=await self.resolve_peer(
                        chat_id if chat_id else m.chat.id
                    ),
                    participant=await self.resolve_peer(
                        user_id if user_id else "self"
                    )
                )
            )
            ).participant

        if isinstance(r, types.ChannelParticipantSelf):
            raise Exception("You can't use this method on yourself.")

        if not isinstance(r, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)):
            raise Exception(f"Invalid type {type(r)}")

        if r is None:
            raise Exception("channels.GetParticipant returned None")

        return getattr(r.admin_rights, privileges)


    async def IsReply(self, message: Message=None):
        """
        Check if the message is a reply to another user.
        """
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        try:
            return message.reply_to_message or m.reply_to_message
        except Exception as e:
            print(e)
        finally:
            del frame


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
        """ get thumbnail of file if it exists """
        thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
        if os.path.exists(thumb_image_path):
            thumb_image_path = os.path.join(self.TEMP_DICT, "thumb_image.jpg")
        elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
            metadata = hachoir.metadata.extractMetadata(
                hachoir.parser.createParser(file_name)
            )
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
        """ run shell commands """
        process = await asyncio.create_subprocess_exec(
            *shell_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        return t_response, e_response


    async def HasteBinPaste(self, text):
        """ paste anything to pasting site """
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

        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)

        globals().update({
            "app": self,
            "bot": getattr(self, "bot", None),
            "reply": m.reply_to_message,
        })
        exec(
            "async def __aexec(self, m): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
        return await locals()["__aexec"](self, m)


    async def error(
        self,
        e: Exception,
        edit_error: bool=True
        ):
        """
        params:
            1. error :: occured exception variable
            2. edit_error: bool, default=True :: edits | sends error message in short

        usage:
            use this function at the end of try/except block

        ex: (async)
            try:
                await app.send_message(message.chat.id, "This is a test")
            except Exception as e:
                await app.error(e, edit_error=False)
        """
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        full_traceback = traceback.format_exc()

        if self.is_bot:
            return print(full_traceback)

        if m:
            teks = "**Traceback Report:**\n\n"
            teks += f"**Date:** `{self.showdate()}`\n"
            teks += f"**Time:** `{self.showtime()}`\n\n"
            teks += f"**Chat Name:** `{m.chat.first_name or m.chat.title}`\n\n"
            teks += f"**Chat Type:** `{m.chat.type.value}`\n\n"
            teks += f"**Message Owner:** `{m.from_user.type.value}`\n\n"
            teks += "`This can be a error in tronuserbot, if you want you can forward this to` @tronUbSupport.\n\n"
            teks += f"**Message:** `{m.text}`\n\n"
            teks += "`-`" * 30 + "\n\n"
            teks += f"**SHORT:** \n\n`{e}`\n\n"
            teks += f"**FULL:** \n\n`{full_traceback}`"
        else:
            teks = ""

        try:
            if edit_error:
                if hasattr(e, "MESSAGE"):
                    await self.send_edit(f"`{e.MESSAGE}`")
                else:
                    await self.send_edit(e.args[0] if e.args else None)

            if len(teks) > 4096:
                await self.create_file("exception.txt", teks)
            else:
                await self.send_message(self.LogChat, teks)

            print(full_traceback)

        except PeerIdInvalid:
            self.log.error(teks)
        except Exception as e:
            self.log.error(e)
        return True


    async def sleep_delete(
        self,
        message=None,
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

        if message:
            m = message
        else:
            frame = inspect.currentframe().f_back
            m = messageobject(frame.f_locals)

        r = None
        await asyncio.sleep(sec)
        if delmsg and m:
            r = await m.delete()
        return r


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
            asyncio.create_task(self.sleep_delete(sec=sec, delmsg=True))
            return True
        else:
            self.log.error("Delete function can only sleep for 10 ( 600 sec ) minutes")


    async def PluginData(
        self,
        module: str
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

            if self.CMD_HELP.get(module) is None:
                r = []
            else:
                r = [
                        f"**CMD:** `{self.Trigger[0]}{cmd}`\n**INFO:** `{usage}`\n\n" 
                        for cmd, usage in zip(
                            self.CMD_HELP.get(module).keys(),
                            self.CMD_HELP.get(module).values()
                        )
                    ]
            return r
        except Exception:
            self.log.error(traceback.format_exc())
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
        entities=None,
        send_as_file: bool=False,
        filename: str=None
        ):
        """
        params:
            1. text: str :: text to be edited or sent instead of editing
            2. disable_web_page_preview: bool, default=False :: web page preview will be shown if True
            3. delme: int, default=0 :: sleeps for given time and then deletes the message

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

        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)

        if (m is None) or (not m):
            return

        try:
            r = None
            file_name = filename or "file.txt"

            if (len(text) > 4096) or send_as_file:
                r = await self.send_edit(
                    "Message text is too long, Sending as file.",
                    text_type=["mono"],
                    delme=3
                )
                return await self.create_file(file_name, text)

            else:
                r = await m.edit(
                    text=self.FormatText(text, textformat=text_type),
                    parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    reply_markup=reply_markup,
                    entities=entities
                )
        except MessageNotModified:
            pass

        except (MessageAuthorRequired, MessageIdInvalid) as e:
            print(traceback.format_exc())
            r = await self.send_message(
                chat_id=m.chat.id,
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

        except Exception as e:
            await self.error(e)

        try:
            if delme > 0:
                self.createThread(
                    self.sleep_delete,
                    message=m, 
                    sec=delme, 
                    delmsg=True
                )

            frame.f_locals["m"] = r # re-asign a new value
            return r # return that new value

        except Exception as e:
            await self.error(e)


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

        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
    
        if m.chat.type == ChatType.PRIVATE:
            await self.send_edit(
                "Please use these commands in groups.",
                text_type=["mono"],
                delme=3
            )
            return True
        return None


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
            frame = inspect.currentframe().f_back
            m = messageobject(frame.f_locals)
            path = f"./downloads/{filename}"
            file = open(path, "w+")
            file.write(content)
            file.close()
            if send:
                await self.send_document(
                    m.chat.id,
                    path,
                    caption = caption if caption else f"**Uploaded By:** {self.UserMention()}"
                )
                if os.path.exists(path):
                    os.remove(path)
                    
                return True
            else:
                return path
        except Exception as e:
            await self.error(e)


    async def kick_user(
        self,
        chat_id: Union[str, int],
        user_id: Union[str, int],
        ban_time: int = 40
        ):
        """
        Kick (noban) a user from chat.

        params::
            chat_id: Union[str, int]
            user_id: Union[str, int]
            ban_time: int = 40

        ex: (async)
            await app.kick_user(
                chat_id,
                user_id,
                ban_time=120
            )
        """

        try:
            return await self.ban_chat_member(
                chat_id,
                user_id,
                datetime.datetime.now() + timedelta(seconds=ban_time))
        except Exception as e:
            await self.error(e)


    async def get_lastmessage(
        self,
        chat_id: Union[int, str],
        reverse: bool = False
        ):
        """
        Get first or last message of a chat.

        params:
            chat_id: Union[int, str]
            reverse: bool = False

        ex: (async)
            await app.get_lastmessage(
                chat_id,
                reverse=True
            )
        """
        try:
            results = [x async for x in self.get_chat_history(chat_id, limit=1)]
            return results[-1] if reverse else results[0]
        except Exception as e:
            await self.error(e)

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
        chat_id: Union[int, str],
        user_id: Union[int, str, List[int], List[str]]
        ):
        """
        Add users in groups/supergroups

        params:
            chat_id: Union[int, str]
            user_id: Union[int, str, List[int], List[str]]
   
        ex: (async)
            await app.add_users(user_id, chat_id)
        """

        try:
            return await self.add_chat_members(
                chat_id,
                user_id
            )
        except Exception as e:
            self.error(e)


    async def user_ingroup(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str]
        ):
        """
        Check if a user exists in group or not.

        params::
            chat_id: Union[int, str]
            user_id: Union[int, str]

        ex: (async)
            await app.user_ingroup(chat_id, user_id)
        """

        async for x in self.get_chat_members(chat_id):
            if x.user.id == user_id:
                return True
        return None



    async def add_logbot(
        self
        ):
        """
        Add you assitant bot in log chat.

        params:
            None

        ex: (async)
            await app.add_logbot()
        """

        try:
            if self.bot:
                if await self.user_ingroup(chat_id, user_id):
                    raise Exception("User is already in group")

                r = await self.add_users(chat_id, user_id)
                return r
            else:
                raise Exception("Bot client is not available")
        except Exception as e:
            await self.error(e)


    async def send_start_message(
        self
        ):
        """ used by bots only """
        try:
            if not self.bot:
                raise BotMethodInvalid

            await self.bot.send_message(
                self.LogChat,
                "The userbot is online now.",
                reply_markup=self.buildMarkup(
                    [self.buildButton(text="Support Group", url="t.me/tronubsupport")]
                )
            )
        except Exception as e:
            print(e)


    async def mute_notification(
        self,
        chat_id: Union[str, int],
        show_previews: bool=None,
        silent: bool=True,
        mute_until: int=None,
        sound: "pyrogram.raw.types.NotificationSound"=None
        ):
        peer = await self.resolve_peer(chat_id)

        return await self.invoke(
            pyrogram.raw.functions.account.UpdateNotifySettings(
                peer=pyrogram.raw.types.InputNotifyPeer(
                    peer=peer
                ),
                settings=pyrogram.raw.types.InputPeerNotifySettings(
                    show_previews=show_previews,
                    silent=silent,
                    mute_until=mute_until,
                    sound=sound
                )
            )
        )


    async def unmute_notification(
        self,
        chat_id: Union[str, int],
        ):
        r = await self.mute_notification(
            chat_id=chat_id,
            show_previews=True,
            silent=False,
            mute_until=None,
            sound=None
        )
        return True if r else False


