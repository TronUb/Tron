""" tools plugin """

from datetime import datetime

from currency_converter import CurrencyConverter

from pyrogram.types import Message

import speedtest

from main import app, gen
from main.core.enums import UserType



c = CurrencyConverter()


# For converting
def convert_f(fahrenheit):
    """ convert f function for tools plugin """
    f = float(fahrenheit)
    return (f*9/5)+32


def convert_c(celsius):
    """ convert c function for tools plugin """
    c = float(celsius)
    return (c-32)*5/9




@app.on_cmd(
    commands="wlink",
    usage="Get message links which contains query word."
)
async def wordlink_handler(_, m: Message):
    """ wordlink handler for tools plugin """
    links = []
    links.clear()

    try:
        if app.long() == 1:
            return await app.send_edit("Please give some text to search in chat ...")

        else:
            messages = await app.get_chat_history(m.chat.id)
            query = m.text.split(None, 1)[1]
            await app.send_edit("Finding word in this chat . . .", text_type=["mono"])
            for msg in messages:
                if query in msg.text:
                    links.append(msg.link)

            await app.send_edit(f"**FOUND LINKS FOR:** `{query}`\n\n" + "\n".join(links))
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands=["cur", "currency"],
    usage="Convert one currency to another currency."
)
async def currency_handler(_, m: Message):
    """ currency handler for tools plugin """
    if app.long() <= 3:
        return await app.send_edit(
            f"Use | `{app.PREFIX}cur 100 USD INR` or `{app.PREFIX}currency 100 USD INR`"
        )

    value = m.command[1]
    cur1 = m.command[2].upper()
    cur2 = m.command[3].upper()
    try:
        await app.send_edit(f"Converting from `{cur1}` to `{cur2}` . . .")
        conv = c.convert(int(value), cur1, cur2)
        text = f"`{value}` `{cur1}` = `{conv:,.2f}` `{cur2}`"
        await app.send_edit(text)
    except ValueError as e:
        await app.error(e)




@app.on_cmd(
    commands=["temp", "temperature"],
    usage="Convert temperatures in Celcius/Fahrenheit."
)
async def temperature_handler(_, m: Message):
    if app.long() <= 2:
        return await app.send_edit(f"How To Use: `{app.MyPrefix()[0]}temp 10 c`", disable_web_page_preview=True)

    temp1 = m.text.split(None, 2)[1]
    temp2 = m.text.split(None, 2)[2]
    try:
        if temp2 == "f":
            result = convert_c(temp1)
            text = "`{}°F` = `{}°C`".format(temp1, result)
            await app.send_edit(text)
        elif temp2 == "c":
            result = convert_f(temp1)
            text = "`{}°C` = `{}°F`".format(temp1, result)
            await app.send_edit(text)
        else:
            await app.send_edit("Unknown type {}".format(temp2))
    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands="json",
    usage="Get json format of a message object (pyrogram)."
)
async def messagejson_handler(_, m: Message):
    reply = m.reply_to_message

    data = str(reply) if reply else str(m)

    try:
        await app.send_edit(data, text_type=["mono"])
    except Exception: # message too long
        m = await app.send_edit("Sending file . . .", text_type=["mono"])
        await app.create_file("json.txt", data)
        if m.from_user.is_self:
            await m.delete()




@app.on_cmd(
    commands="mlink",
    usage="Get a message link of a message."
)
async def messagelink_handler(_, m: Message):
    reply = m.reply_to_message
    message = reply if reply else m

    m = await app.send_edit("Generating message link . . .", text_type=["mono"])
    await app.send_edit(message.link)




@app.on_cmd(
    commands="saved",
    usage="Save a text, media in saved messages.",
    disable_for=UserType.SUDO
)
async def saved_handler(_, m: Message):
    if m.from_user.is_self:
        await m.delete()
    await m.reply_to_message.copy("me")




@app.on_cmd(
    commands=["fwd", "frwd"],
    usage="Forward a message."
)
async def forward_handler(_, m: Message):
    reply = m.reply_to_message
    try:

        if reply and app.long() == 1:
            await reply.forward(m.chat.id)
            delete = True

        elif reply and app.long() > 1:
            await reply.forward(m.command[1])
            delete = True

        elif not reply and app.long() == 1:
            await m.forward(m.chat.id)
            delete = True

        elif not reply and app.long() > 1:
            await app.send_edit("Sir reply to yours or someone's message. to forward.", text_type=["mono"], delme=4)
            delete = False

        else:
            await app.send_edit("Something went wrong, please try again later !", text_type=["mono"], delme=4)
            delete = False

        if m.from_user.is_self and delete:
            await m.delete()

    except Exception as e:
        await app.error(e)




@app.on_cmd(
    commands=["spt", "speed", "speedtest"],
    usage="Get upload/download speed."
)
async def speedtest_handler(_, m: Message):
    if app.long() == 1:
        await app.send_edit("Testing speed . . .", text_type=["mono"])
        test = speedtest.Speedtest()
        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()
        teks = "**⧓ Speed Test Results ⧓**\n\n"
        teks += "**DOWNLOAD ⊢** `{}`\n".format(app.SpeedConvert(result['download']))
        teks += "**UPLOAD ⊢** `{}`\n".format(app.SpeedConvert(result['upload']))
        teks += "**PING ⊢** `{} ms`\n".format(result['ping'])
        teks += "**SERVER ⊢** `{}`\n".format(result['client']['isp'])
        teks += "**LOCATION ⊢** `{}, {}`".format(result['server']['name'], result['server']['country'])
        if teks:
            await app.send_edit(teks)
        else:
            await app.send_edit("Something went wrong !", text_type=["mono"], delme=5)
    elif app.long() > 1 and "pic" in m.command[1]:
        await app.send_edit("Calculating Speed (pic) . . .")

        start = datetime.now()
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        response = s.results.dict()
        download = response.get("download")
        upload = response.get("upload")
        ping = response.get("ping")
        agent = response.get("client")
        isp = agent.get("isp")
        isp_rating = agent.get("isprating")
        response = s.results.share()
        speedtest_image = response
        if speedtest_image:
            await app.send_photo(
                m.chat.id,
                speedtest_image,
                caption="**Time Taken:** {} ms".format(ms),
                parse_mode="markdown"
            )
            await m.delete()
        else:
            await app.send_edit("Something went wrong !", text_type=["mono"], delme=5)





@app.on_cmd(
    commands=["cc", "cchats"],
    usage="Get list of common chats with a user."
)
async def commonchat_handler(_, m):
    try:
        reply = m.reply_to_message
        if reply:
            collect = []
            collect.clear()

            data = await app.get_common_chats(reply.from_user.id)
            for x in data:
                collect.append(getattr(x, "title") + "\n")
            if bool(collect):
                await app.send_edit(f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "".join(collect))
            else:
                await app.send_edit(f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "`None`")
        else:
            await app.send_edit("Please reply to someone . . .", text_type=["mono"], delme=4)
    except Exception as e:
        await app.error(e)
