""" supertools plugin """

import os
from html import escape
import requests

from gtts import gTTS

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"supertools" : (
        "supertools",
        {
        "ud [query]" : "Get The Meaning Of Any Word In Urban Dictionary.",
        "short [link]" : "Shorten a link into da.gd link.",
        "unshort [shortlink]" : "Reverse the da.gd link to real link.",
        "tts [reply to text]" : "Text To Speech, Convert Text Message To Voice | audio (mp3).",
        "wtr [city name]" : "Type Command And Your City Name To Get Weather Details.",
        "ws [site link]" : "Take A Screenshot Of Any Website And Get The Image Of That Site.",
        "undlt [count]" : "Get deleted messages from recent history of group . . .",
        }
        )
    }
)


weather_lang_code="en"

lang_code = os.getenv("LANG_CODE", "en")


def replace_text(text):
    """ replace text function for supertools plugin """
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


async def text_to_voice(m: Message, text):
    """ text to voice function for supertools plugin """
    tts = gTTS(text, lang=lang_code)
    tts.save(f"{app.TEMP_DICT}voice.mp3")
    await app.send_voice(
        m.chat.id,
        voice=f"{app.TEMP_DICT}voice.mp3",
        reply_to_message_id=m.id
        )
    await m.delete()
    os.remove(f"{app.TEMP_DICT}voice.mp3")
    return




async def shorten_link(m: Message, text):
    """ shorten link function for supertools plugin """
    sample_url = f"https://da.gd/s?url={text}"
    response = requests.get(sample_url).text
    if response:
        await app.send_edit(
            m,
            f"**Generated Link:**\n\nShorted Link: {response}\nYour Link: {text}",
            disable_web_page_preview=True)
    else:
        await app.send_edit(m, "something is wrong. please try again later.", text_type=["mono"])




async def unshorten_link(m: Message, text):
    """ unshorten link function for supertools plugin """
    if not text.startswith("https://da.gd/"):
        await app.send_edit(m, "Please Give me a valid link that starts with `https://da.gd/`")
    else:
        r = requests.get(
            text,
            exclude_redirects=False
        )
        if str(r.status_code).startswith("3"):
            fakelink = r.headers["Location"]
            await app.send_edit(
                f"**Generated Links:**\n\nUnshorted Link: {fakelink}\nYour Link: {text}",
                disable_web_page_preview=True
            )
        else:
            await app.send_edit(
                "Something went wrong, please try again later . . .",
                text_type=["mono"]
            )




@app.on_message(gen("tts"))
async def tts_handler(_, m: Message):
    """tts handler for supertools plugin """
    reply = m.reply_to_message

    try:
        if not reply and app.long() == 1:
            return await app.send_edit("Reply to someone's text message or give me the text as a suffix . . .", delme=True, text_type=["mono"])

        elif not reply and app.long() > 1:
            await app.send_edit("Converting text to voice . . .", text_type=["mono"])
            text = m.text.split(None, 1)[1]
            await text_to_voice(m, text)

        elif reply:
            if not reply.text:
                return await app.send_edit("Please reply to a text . . .", text_type=["mono"], delme=3)
            await app.send_edit("Converting text to voice . . .", text_type=["mono"])
            text = reply.text
            await text_to_voice(m, text)

        else:
            await app.send_edit("Something went wrong !", text_type=["mono"])
    except Exception as e:
        await app.error(e)




@app.on_message(gen("ud"))
async def ud_handler(_, m:Message):
    """ ud_handler for supertools plugin """
    if app.long() == 1:
        return await app.send_edit(f"Use: `{app.PREFIX}ud cats`")

    try:
        await app.send_edit(f"Searching for `{m.text.split(None, 1)[1]}`")
        text = m.text.split(None, 1)[1]
        response = await app.GetRequest(
            f"http://api.urbandictionary.com/v0/define?term={text}"
        )
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        resp = (
            f"**Text**: __`{replace_text(word)}`__\n\n"
            f"**Meaning:**\n\n`{replace_text(definition)}`\n\n"
            f"**Example:**\n\n`{replace_text(example)}` "
        )
        await app.send_edit(resp)
    except IndexError:
        await app.send_edit("No Results Found !", text_type=["mono"], delme=3)
    except Exception as e:
        await app.error(e)




@app.on_message(gen("short"))
async def shortlink_handler(_, m: Message):
    """ shortlink handler for supertools plugin """
    reply = m.reply_to_message
    try:
        if not reply and app.long() == 1:
            return await app.send_edit(
                "Please give me some link or reply to a link",
                text_type=["mono"]
            )

        if not reply and app.long() > 1:
            text = m.text.split(None, 1)[1]
            await shorten_link(m, text)
        elif reply:
            if not reply.text:
                return await app.send_edit("Please reply to text . . .", text_type=["mono"])
            text = reply.text
            await shorten_link(m, text)
    except Exception as e:
        await app.error(e)




@app.on_message(gen(["unshort", "noshort"]))
async def unshortlink_handler(_, m: Message):
    """ unshortlink handler for supertools plugin """
    reply = m.reply_to_message
    try:
        if not reply and app.long() == 1:
            return await app.send_edit(
                "Please give me a da.gd link to convert to orginal link",
                text_type=["mono"]
            )

        elif not reply and app.long() > 1:
            text = m.text.split(None, 1)[1]
            await unshorten_link(m, text)

        elif reply:
            if not reply.text:
                return await app.send_edit("Please reply to a text . . .", text_type=["mono"])
            text = reply.text
            await unshorten_link(m, text)

        else:
            await app.send_edit("Something went wrong, try again later !", text_type=["mono"])
    except Exception as e:
        await app.error(e)




@app.on_message(gen(["wtr", "weather"]))
async def weather_handler(_, m: Message):
    """ whether handler for supertools plugin """
    if app.long() == 1:
        return await app.send_edit(
            "Piro Master Atleast Give Me Some Location !",
            text_type=["mono"]
        )

    await app.send_edit("Checking weather . . .", text_type=["mono"])
    location = m.command[1]
    headers = {'user-agent': 'httpie'}
    response = requests.get(
        f"https://wttr.in/{location}?mnTC0&lang={weather_lang_code}",
        headers=headers
    )
    if "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity." in response.text:
        return await app.send_edit("Too many requests, try again later !", text_type=["mono"])

    weather = f"__{escape(response.text)}__"
    await app.send_edit(weather)




@app.on_message(gen(["ws", "webshot"]))
async def webshot_handler(_, m: Message):
    """ webshot handler for supertools plugin """
    if app.long() > 1:
        try:
            BASE = "https://render-tron.appspot.com/screenshot/"
            url = m.command[1]
            path = "./downloads/screenshot.jpg"
            response = requests.get(BASE + url, stream=True)

            if response.status_code == 200:
                with open(path, "wb") as file:
                    for chunk in response:
                        file.write(chunk)
            await app.send_edit("generating pic . . .", text_type=["mono"])
            await app.send_document(
                m.chat.id,
                path,
                caption=url
                )
            await m.delete()
            os.remove(path)
        except Exception as e:
            await app.error(e)
    else:
        await app.send_edit("Give me the link pro . . .", text_type=["mono"])




@app.on_message(gen("undlt"))
async def undlt_handler(_, m: Message):
    """ undlt handler for supertools plugin """
    collect = []
    collect.clear()

    if app.long() == 1:
        count = 5
    elif app.long() > 1:
        count = m.command[1]
        if count.isdigit():
            count = int(count)
        else:
            count = 5
    try:
        async for x in app.get_chat_history(m.chat.id, limit=count):
            if x.text:
                collect.append(f"**Message:** `{x.text}`\n\n")
        await app.send_edit("".join(collect))
    except Exception as e:
        await app.error(e)
