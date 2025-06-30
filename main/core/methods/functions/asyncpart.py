import os
import math
import json
import random
import asyncio
import inspect
import traceback
import datetime
import aiohttp
from time import time
from datetime import timedelta
from typing import List, Union
from pyrogram.raw import functions, types
from pyrogram.errors import (
    BotMethodInvalid,
    MessageNotModified,
    FloodWait,
    YouBlockedUser,
    MessageAuthorRequired,
    MessageIdInvalid,
)
from pyrogram.enums import ParseMode, ChatType
from pyrogram.types import Message


# pylint: disable=E1101


def messageobject(anydict: dict):
    all_messages = [x for x in anydict.values() if isinstance(x, Message)]
    try:
        return all_messages[0]
    except IndexError:
        return None


class AsyncPart:

    async def GetRequest(self, url: str, resptype: str = "json"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    if resptype == "jsontext":
                        return json.loads(await resp.text())
                    return await getattr(resp, resptype)()
                except Exception:
                    return json.loads(await resp.text())

    async def PostRequest(
        self, endpoint: str, payload: dict, timeout: int = 3, resptype: str = "json"
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint, data=payload, timeout=timeout
            ) as response:
                return await response.json()

    async def IsAdmin(self, privileges: str = "ban_users", chat_id=None, user_id=None):
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        r = (
            await self.invoke(
                functions.channels.GetParticipant(
                    channel=await self.resolve_peer(chat_id or m.chat.id),
                    participant=await self.resolve_peer(user_id or "self"),
                )
            )
        ).participant
        if isinstance(r, types.ChannelParticipantSelf):
            raise Exception("You can't use this method on yourself.")
        if not isinstance(
            r, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator)
        ):
            raise Exception(f"Invalid type {type(r)}")
        return getattr(r.admin_rights, privileges)

    async def IsReply(self, message: Message = None):
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        try:
            return message.reply_to_message or m.reply_to_message
        except Exception as e:
            print(e)

    async def ProgressForPyrogram(self, current, total, ud_type, message, start):
        now = time()
        diff = now - start
        if round(diff % 10.00) == 0 or current == total:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = elapsed_time + time_to_completion
            progress = "**[{0}{1}]** \n**Progress**: __{2}%__\n".format(
                "".join(["●" for _ in range(math.floor(percentage / 5))]),
                "".join(["○" for _ in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
            tmp = (
                progress
                + "**Done:** __{0} of {1}__\n**Speed:** __{2}/s__\n**ETA:** __{3}__\n".format(
                    self.HumanBytes(current),
                    self.HumanBytes(total),
                    self.HumanBytes(speed),
                    self.TimeFormator(milliseconds=estimated_total_time) or "0 s",
                )
            )
            try:
                await message.edit(f"{ud_type}\n {tmp}")
            except (MessageNotModified, FloodWait):
                pass

    async def aexec(self, code: str):
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        globals().update({"app": self, "reply": m.reply_to_message})
        exec(
            "async def __aexec(self, m): "
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
        return await locals()["__aexec"](self, m)

    async def error(self, e: Exception, edit_error: bool = True):
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        full_traceback = traceback.format_exc()
        print(full_traceback)
        if self.is_bot:
            return
        if edit_error and m:
            await self.send_edit(str(e))
        if len(full_traceback) > 4096:
            await self.create_file("exception.txt", full_traceback)
        else:
            await self.send_message(self.LogChat, f"```{full_traceback}```")
        return True

    async def sleep_delete(self, message=None, sec: int = 0, delmsg=False):
        if self.is_bot:
            raise BotMethodInvalid
        frame = inspect.currentframe().f_back
        m = message or messageobject(frame.f_locals)
        await asyncio.sleep(sec)
        if delmsg and m:
            await m.delete()

    async def create_file(
        self, filename: str, content: str, send: bool = True, caption: str = None
    ):
        frame = inspect.currentframe().f_back
        m = messageobject(frame.f_locals)
        path = f"./downloads/{filename}"
        with open(path, "w+", encoding="utf-8") as f:
            f.write(content)
        if send:
            await self.send_document(m.chat.id, path, caption=caption or "Uploaded")
            if os.path.exists(path):
                os.remove(path)
            return True
        return path
