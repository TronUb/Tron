""" all synchronous functions are stored here """

import re
import os
import time
import math
import datetime
import html
import subprocess
import importlib

from typing import List

from pyrogram.types import (
    Message,
    InlineKeyboardButton
)
from pyrogram.errors import BotMethodInvalid

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from PIL import Image
import heroku3
import requests
import pytz

from pySmartDL import SmartDL






class Types(object):
    TEXT = 1
    DOCUMENT = 2
    PHOTO = 3
    VIDEO = 4
    STICKER = 5
    AUDIO = 6
    VOICE = 7
    VIDEO_NOTE = 8
    ANIMATION = 9
    ANIMATED_STICKER = 10
    CONTACT = 11



class SyncPart(Types):
    def showdate(
        self
        ):
        """
        params:
            None

        use:
            use this function to get realtime date of your location

        ex: (async)
            await app.showdate()
        """

        today = pytz.timezone(self.TIME_ZONE)
        get_date = datetime.datetime.now(today)
        mydate = get_date.strftime("%d %b %Y")
        return mydate


    def showtime(
        self
        ):
        """
        params:
            None

        use:
            use this function to get time of your location

        ex: (async)
            await app.showtime()
        """

        today = pytz.timezone(self.TIME_ZONE)
        get_time = datetime.datetime.now(today)
        mytime = get_time.strftime("%r")
        return mytime


    def long(
        self
        ):
        """
        params:
            None

        use:
            this function returns the length of a list containing message splited on spaces

        ex:
            if app.long() == 1:
                print("there is one word in message.text")
        """
        if self.is_bot:
            raise BotMethodInvalid

        text_length = len(self.m.text.split() or self.m.caption.split())
        return text_length if bool(text_length) is True else None


    def textlen(
        self
        ):
        """
        params:
            None

        use:
            this function returns length of characters in message.text

        ex:
            if app.textlen() > 4096:
                print("Text is too long")
        """
        if self.is_bot:
            raise BotMethodInvalid

        return len([x for x in self.m.text or self.m.caption or []])


    def rem_dual(
        self,
        list1: list,
        list2: list
        ):
        """
        params:
            1. one: list :: list from that you want to remove duplicates
            2. two: list :: list that contains removable elements

        use:
            use this function to remove duplicates from lists

        ex:
            app.rem_dual([1, 1, 1, 2, 3], [1])
        """

        return list(set(list1) - set(list2))


    def is_str(
        self,
        element
        ):
        """
        params:
            1. element: [str, bool, int, float] :: anytype of data

        use:
            use this function to check if the element is string or not

        ex:
            app.is_str(data)
        """

        return isinstance(element, str)


    def is_bool(
        self,
        element
        ):
        """
        params:
            1. element: [str, bool, int, float] :: anytype of data

        use:
            use this function to check if the element is boolean or not

        ex:
            app.is_bool(data)
        """

        return isinstance(element, bool)


    def is_float(
        self,
        element
        ):
        """
        params:
            1. element: [str, bool, int, float] :: anytype of data

        use:
            use this function to check if the element is float or not

        ex:
            app.is_float(data)
        """

        return isinstance(element, float)


    def is_int(
        self,
        element
        ):
        """
        params:
            1. element: [str, bool, int, float] :: anytype of data

        use:
            use this function to check if the element is integer or not

        ex:
            app.is_int(data)
        """

        return isinstance(element, int)


    def quote(
        self
        ):
        """
        params:
            None

        use:
            use this function to anime quotes

        ex:
            app.quote()
        """

        results = requests.get("https://animechan.vercel.app/api/random").json()
        msg = f"❝ {results.get('quote')} ❞"
        msg += f" [ {results.get('anime')} ]\n\n"
        msg += f"- {results.get('character')}\n\n"
        return msg


    def ialive_pic(
        self
        ):
        """
        params:
            None

        use:
            use this function to get inline alive pic url

        ex:
            app.ialive_pic()
        """

        return self.getdv("USER_PIC") or self.UserPic() or None


    def get_file_id(
        self,
        message: Message
        ):
        """
        params:
            1. message (update) :: incoming update

        use:
            use this function to get file_id of any media in telegram

        ex:
            app.get_file_id(message)
        """

        media = ["photo", "video", "audio", "document", "sticker", "animation"]

        for x in media:
            if message and getattr(message, x, False):
                if getattr(message, "caption"):
                    return {"data":(getattr(message, x)).file_id, "caption":message.caption, "type":x}
                else:
                    return {"data":(getattr(message, x)).file_id, "caption":None, "type":x}
            elif getattr(message, "text", False):
                return {"data":message.text, "caption":None, "type":"text"}
        return {"data":None, "caption":None, "type":None}


    def clear_screen(
        self
        ):
        """
        params:
            None

        use:
            use this function to clear terminal screen

        ex:
            app.clear_screen()
        """

        subprocess.call("clear" if os.name == "posix" else "cls")


    def uptime(
        self
        ):
        """
        params:
            None

        use:
            use this function to get ubot uptime

        ex:
            app.uptime()
        """

        return self.GetReadableTime(time.time() - self.StartTime)


    def import_module(
        self,
        path: str,
        exclude: list=[],
        display_module: bool=True
        ):
        """
        params:
            1. path :: path of module directory
            2. exclude: list, default=[] :: exclude specific module installation
            3. display_module: bool, drfau=True :: whether to print module name after installation or not

        use:
            use this function to install python modules

        ex:
            app.import_module("./tronx/modules/", exclude=["admin"])
        """

        listbin = []
        listbin.clear()

        if not os.path.exists(path):
            return self.log.info(f"No path found: {path}")

        modules = []
        modules.clear()

        for x in os.listdir(path):
            if x.endswith(".py"):
                if not x in ["__pycache__",  "__init__.py"]:
                    modules.append(x.replace(".py", ""))

        py_path_raw = ".".join(path.split("/"))
        py_path = py_path_raw[0:len(py_path_raw)-1]

        count = 0
        for x in modules:
            if not x in exclude:
                importlib.import_module(py_path + "." + x)
                count += 1
                listbin.append(x)

        if display_module:
            data = sorted(listbin)
            for x in data:
                print(x + " Loaded !")
        return count


    def db_status(
        self
        ):
        """
        params:
            None

        use:
            use this function to check if database is available or not

        ex:
            app.db_status()
        """

        return "Available" if hasattr(self, "DB_URI") and self.DB_URI else "Unavailable"


    def heroku_app(self):
        """
        params:
            None

        use:
            use this function to get acess of your heroku app

        ex:
            app.heroku_app()
        """
        if not (self.HerokuApiKey() and self.HerokuAppName()):
            return None

        account = heroku3.from_key(self.HerokuApiKey())
        return account.apps()[self.HerokuAppName()]


    def HelpDex(self, page_number, allmodules, prefix):
        rows = 4
        column = 2
        help_modules = []
        for mod in allmodules:
            if not mod.startswith("_"):
                help_modules.append(mod)
        help_modules = sorted(help_modules)
        modules = [
            InlineKeyboardButton(
                text="{} {}".format(
                    self.HelpEmoji(),
                    x.replace("_", " ").title(),
                ),
                callback_data="pluginlist-{}|{}".format(x, page_number),
            )
            for x in help_modules
        ]
        twins = list(zip(modules[::column], modules[1::column]))
        if len(modules) % column == 1:
            twins.append((modules[-1],))
        num_pages = math.ceil(len(twins) / rows)
        mod_page = page_number % num_pages
        if len(twins) > rows:
            twins = twins[
                mod_page * rows : rows * (mod_page + 1)
            ] + [
                (
                    InlineKeyboardButton(
                        text="❰ Prev",
                        callback_data="{}-prev({})".format(
                            prefix, mod_page
                        ),
                    ),
                    InlineKeyboardButton(text="Back", callback_data="home-tab"),
                    InlineKeyboardButton(
                        text="Next ❱",
                        callback_data="{}-next({})".format(
                            prefix, mod_page
                        ),
                    ),
                )
            ]
        return twins


    def GetMessageType(self, msg, include_text=True):
        content = None
        message_type = None

        if include_text is True:
            if msg.text or msg.caption:
                content = msg
                message_type = Types.TEXT

        elif msg.sticker:
            content = msg.sticker.file_id
            message_type = Types.STICKER

        elif msg.document:
            if msg.document.mime_type == "application/x-bad-tgsticker":
                message_type = Types.ANIMATED_STICKER
            else:
                message_type = Types.DOCUMENT
            content = msg.document.file_id

        elif msg.photo:
            content = msg.photo.file_id  # last elem = best quality
            message_type = Types.PHOTO

        elif msg.audio:
            content = msg.audio.file_id
            message_type = Types.AUDIO

        elif msg.voice:
            content = msg.voice.file_id
            message_type = Types.VOICE

        elif msg.video:
            content = msg.video.file_id
            message_type = Types.VIDEO

        elif msg.video_note:
            content = msg.video_note.file_id
            message_type = Types.VIDEO_NOTE

        elif msg.animation:
            content = msg.animation.file_id
            message_type = Types.ANIMATION
        return content, message_type


    def GetNoteType(self, msg):
        reply = msg.reply_to_message
        note_name = None
        message_type = None
        content = None
        text = None

        if self.long() == 1:
            return None, None, None, None, None

        if msg.text:
            raw_text = msg.text.markdown
        elif msg.caption:
            raw_text = msg.caption.markdown
        else:
            raw_text = None

        note_name = raw_text.split()[1]

        # determine what the contents of the filter are - text, image, sticker, etc
        if self.long() >= 3:
            text = raw_text.split(None, 2)[2]
            message_type = Types.TEXT

        elif reply:
            if reply.text:
                text = reply.text.markdown if reply.text else reply.caption.markdown if reply.caption else ""
                message_type = Types.TEXT
                content, message_type = self.GetMessageType(reply, include_text=False)
            else:
                return

        return note_name, text, message_type, content


    def FetchNoteType(self, msg):
        message_type = None
        content = None
        note_name = None
        text = None

        if msg:
            if msg.text:
                text = msg.text.markdown if msg.text else msg.caption.markdown if msg.caption else ""
                message_type = Types.TEXT

            content, message_type = self.GetMessageType(msg, include_text=False)

        return note_name, text, message_type, content


    def ClearString(self, msg: str):
        msg = re.sub(r"\<code\>(.*)\<\/code\>", "\g<1>", msg)
        msg = re.sub(r"\<i\>(.*)\<\/i\>", "\g<1>", msg)
        msg = re.sub(r"\<b\>(.*)\<\/b\>", "\g<1>", msg)
        msg = re.sub(r"\<u\>(.*)\<\/u\>", "\g<1>", msg)
        msg = re.sub(r"\*\*(.*)\*\*", "\g<1>", msg)
        msg = re.sub(r"\_\_(.*)\_\_", "\g<1>", msg)
        msg = re.sub(r"\`(.*)\`", "\g<1>", msg)
        return msg


    def QuoteHtml(self, text: str) -> str:
        """
        Escape unexpected HTML characters.
        :param text: Original text
        :return:
        """
        return html.escape(text, quote=False)


    def TimeFormator(self, milliseconds: int) -> str:
        """ converts seconds into human readable format """
        seconds, milliseconds = divmod(int(milliseconds), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = (
            ((str(days) + "d, ") if days else "")
            + ((str(hours) + "h, ") if hours else "")
            + ((str(minutes) + "m, ") if minutes else "")
            + ((str(seconds) + "s, ") if seconds else "")
            + ((str(milliseconds) + "ms, ") if milliseconds else "")
        )
        return tmp[:-2]


    def HumanBytes(self, size: int) -> str:
        """ converts bytes into human readable format """
        if not size:
            return ""
        power = 2 ** 10
        number = 0
        dict_power_n = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
        while size > power:
            size /= power
            number += 1
        return str(round(size, 2)) + " " + dict_power_n[number] + "B"


    def DictSizeInBytes(self, directory):
        """Returns the `directory` size in bytes."""
        total = 0
        try:
            # print("[+] Getting the size of", directory)
            for entry in os.scandir(directory):
                if entry.is_file():
                    # if it's a file, use stat() function
                    total += entry.stat().st_size
                elif entry.is_dir():
                    # if it's a directory, recursively call this function

                    total += self.DictSizeInBytes(entry.path)
        except NotADirectoryError:
            # if `directory` isn't a directory, get the file size then
            return os.path.getsize(directory)
        except PermissionError:
            # if for whatever reason we can't open the folder, return 0
            return 0
        return total


    def SizeFormat(self, b, factor=1024, suffix="B"):
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


    def DictSize(self, location):
        return self.SizeFormat(self.DictSizeInBytes(location))


    def CleanHtml(self, raw_html):
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, "", raw_html)
        return cleantext


    def EscapeMarkdown(self, text):
        escape_chars = r"\*_`\["
        return re.sub(r"([%s])" % escape_chars, r"\\\1", text)


    def MentionHtml(self, user_id, name):
        return '<a href="tg://user?id={}">{}</a>'.format(user_id, html.escape(name))


    def MentionMarkdown(self, user_id, name):
        return '[{}](tg://user?id={})'.format(self.EscapeMarkdown(name), user_id)


    def ParseButton(self, text):
        markdown_note = text
        prev = 0
        note_data = ""
        buttons = []
        BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")
        for match in BTN_URL_REGEX.finditer(markdown_note):
            # Check if btnurl is escaped
            n_escapes = 0
            to_check = match.start(1) - 1
            while to_check > 0 and markdown_note[to_check] == "\\":
                n_escapes += 1
                to_check -= 1

            # if even, not escaped -> create button
            if n_escapes % 2 == 0:
                # create a thruple with button label, url, and newline status
                buttons.append((match.group(2), match.group(3), bool(match.group(4))))
                note_data += markdown_note[prev:match.start(1)]
                prev = match.end(1)
            # if odd, escaped -> move along
            else:
                note_data += markdown_note[prev:to_check]
                prev = match.start(1) - 1
        else:
            note_data += markdown_note[prev:]

        return note_data, buttons


    def BuildKeyboard(self, buttons):
        keyb = []
        keyb.clear()

        for btn in buttons:
            keyb.append(
                    InlineKeyboardButton(
                        btn[0],
                        callback_data=btn[1]
                    )
            )
        return keyb


    def TimeParser(self, start, end=None) -> int:
        if end is None:
            time_end = start
        else:
            time_end = end - start
        month = time_end // 2678400
        days = time_end // 86400
        hours = time_end // 3600 % 24
        minutes = time_end // 60 % 60
        seconds = time_end % 60
        times = ""
        if month:
            times += "{} month, ".format(month)
        if days:
            times += "{} days, ".format(days)
        if hours:
            times += "{} hours, ".format(hours)
        if minutes:
            times += "{} minutes, ".format(minutes)
        if seconds:
            times += "{} seconds".format(seconds)
        if times == "":
            times = "{} miliseconds".format(time_end)
        return times


    def ConvertSize(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])


    def GetArgs(self, message=None):
        reply = self.m.reply_to_message

        if message:
            return message

        elif reply:
            setattr(
                reply,
                "text",
                self.m.text.split(None, 1)[0] + " " + reply.text
            )
            return reply

        elif not reply:
            if self.long() > 1:
                return self.m
        return type("argclass", (object,), {"text" : None})()


    def SpeedConvert(self, bytesize) -> str:
        " converts bytes into kb, mb, gb, tb "
        power = 2**10 # 1024
        zero = 0
        units = {
            0: '',
            1: 'Kb/s',
            2: 'Mb/s',
            3: 'Gb/s',
            4: 'Tb/s'}
        while bytesize > power:
            bytesize /= power
            zero += 1
        return f"{round(bytesize, 2)} {units[zero]}"


    def GetReadableTime(self, seconds: int) -> str:
        " get time formated from seconds "
        count = 0
        ping_time = ""
        time_list = []
        time_suffix_list = ["s", "m", "h", "days"]

        while count < 4:
            count += 1
            remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
            if seconds == 0 and remainder == 0:
                break
            time_list.append(int(result))
            seconds = int(remainder)

        for x in range(len(time_list)):
            time_list[x] = str(time_list[x]) + time_suffix_list[x]
        if len(time_list) == 4:
            ping_time += time_list.pop() + ", "

        time_list.reverse()
        ping_time += ":".join(time_list)

        return ping_time


    def GenTgThumb(self, downloaded_file_name: str) -> str:
        " generates thumbnail of downloaded telegram media "
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        img = Image.open(downloaded_file_name)
        img.resize((320, height))
        img.save(downloaded_file_name, "JPEG")
        return downloaded_file_name


    def ChatType(self, m: Message):
        " get chat type "
        return m.chat.type


    def FormatText(self, text, textformat=[]):
        " get formated text (html) "
        for x in textformat:
            format_dict = {
            "mono" : f"<code>{text}</code>",
            "bold" : f"<b>{text}</b>",
            "italic" : f"<i>{text}</i>",
            "strike" : f"<s>{text}</s>",
            "underline" : f"<u>{text}</u>"
            }
            text = format_dict.get(x)
        return text


    def PyDownload(self, url: str):
        obj = SmartDL(url, self.TEMP_DICT, progress_bar=False)
        obj.start()
        return obj.get_dest()
