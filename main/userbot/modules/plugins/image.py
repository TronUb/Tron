""" image plugin """

import os
import json
import asyncio
import qrcode
import requests

from PIL import Image

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
    {"image" : (
        "image",
        {
        "uns [ query ]" : "Search Images On Unsplash.",
        "stoi [ reply to sticker ]" : "Converts the replied sticker into image.",
        "itos [ reply to image ]" : "Converts the replied image into sticker.",
        "qc [ text ]" : "Creates a qr code image.",
        "colour [ colour name ] [ text ]" : "Creates a colour background image.",
        "cat" : "Get random cat images.",
        "waifu" : "Get random waifu images.",
        "poto" : "Get profile photos of yours or someone's else.",
        "dog" : "Get random dog images.",
        }
        )
    }
)


# colour code to generate images
COLOUR_CODE = {
    "aqua": "rgba(0, 255, 255, 100)",
    "red": "rgba(255, 0, 0, 100)",
    "blue": "rgba(0, 0, 255, 100)",
    "green": "rgba(0, 255, 0, 100)",
    "yellow": "rgba(255, 255, 0, 100)",
    "gold": "rgba(255, 215, 0, 100)",
    "orange": "rgba(255, 165, 0, 100)",
    "purple": "rgba(41, 5, 68, 100)",
    "black": "rgba(0, 0, 0, 100)",
    "white": "rgba(255, 255, 255, 100)",
}




async def get_image(m: Message, keyword):
    """ getimage function for image plugin """
    await app.send_edit(
        "Getting Picture . . .",
        text_type=["mono"]
        )
    img = await app.get_url(
        f"https://source.unsplash.com/1600x900/?{keyword}"
        )
    await asyncio.gather(
        m.delete(),
        app.send_photo(m.chat.id, str(img))
        )




async def send_profile_pic(m):
    """ sendprofilepic function for image plugin """
    reply = m.reply_to_message
    ids = reply.from_user.id if reply else "me"

    async for x in app.get_chat_photos(ids):
        await app.send_cached_media(m.chat.id, x.file_id)



@app.on_message(gen(["uns", "unsplash"]))
async def unsplash_handler(_, m: Message):
    """ unsplash handler for image """
    cmd = m.command
    if app.long() == 1:
        await app.send_edit(
            "Give me some query after command . . .",
            text_type=["mono"],
            delme=4
        )
    elif app.long() == 2:
        if cmd[1].isdigit():
            return await app.send_edit(
                "Sorry but give me a text query.",
                text_type=["mono"],
                delme=4
            )
        else:
            keyword = cmd[1]
        await get_image(m, keyword)
    elif app.long() > 2:
        images = []
        images.clear()
        if cmd[1].isdigit():
            if app.is_str(cmd[2]):
                await app.send_edit("Getting images . . .", text_type=["mono"])
                second = int(cmd[1]) + 1
                keyword = cmd[2]
                for _ in range(1, second):
                    img = await app.get_url(
                        f"https://source.unsplash.com/1600x900/?{keyword}"
                        )
                    images.append(img)

                await app.send_edit("Getting image . . .", text_type=["mono"])
                for img in images:
                    await asyncio.gather(
                        app.send_photo(m.chat.id, str(img))
                        )
                if m.from_user.is_self:
                    await m.delete()
            else:
                await app.send_edit(
                    "Sorry numbers are not excludeed to be a search query.",
                    delme=4,
                    text_type=["mono"]
                )
        else:
            await app.send_edit(
                "Give me count number of how many images you need.",
                delme=4,
                text_type=["mono"]
            )
    else:
        return app.send_edit("Something went wrong !", text_type=["mono"], delme=4)




@app.on_message(gen("stoi"))
async def stoi_handler(_, m):
    """ stoi handler for image plugin """
    reply = m.reply_to_message
    if not reply:
        await app.send_edit("reply to a sticker.", text_type=["mono"], delme=3)

    elif reply:
        if reply.sticker:
            if not reply.sticker.is_animated:
                filename = f"{app.TEMP_DICT}sticker.jpg"
                msg = await app.send_edit("Converting To Image ...", text_type=["mono"])
                await app.download_media(
                    message=reply,
                    file_name=filename
                    )
                await app.send_photo(
                    m.chat.id,
                    filename,
                    reply_to_message_id=reply.id
                    )
                await msg.delete()
                if os.path.exists(filename):
                    os.remove(filename)
            else:
                await app.send_edit(
                    "Animated Stickers are Not Supported!",
                    delme=3,
                    text_type=["mono"]
                )
        else:
            await app.send_edit("Reply to a sticker please !", delme=3, text_type=["mono"])




@app.on_message(gen("itos"))
async def itos_handler(_, m):
    """ itos handler for image plugin """
    reply = m.reply_to_message
    if not reply:
        await app.send_edit("Reply to a image.", text_type=["mono"], delme=3)

    elif reply:
        if reply.photo or reply.document.file_name.endswith(".png" or ".jpg" or "jpeg"):
            if not reply.video:
                await app.send_edit("Converting To Sticker . . .", text_type=["mono"])
                filename = f"{app.TEMP_DICT}sticker.webp"
                await app.download_media(
                    message=reply,
                    file_name=filename
                    )
                await app.send_sticker(
                    m.chat.id,
                    filename,
                    reply_to_message_id=reply.id)
                await m.delete()
                if os.path.exists(filename):
                    os.remove(filename)
            else:
                await app.send_edit(
                    "video and animated Stickers Not Supported!",
                    delme=3,
                    text_type=["mono"]
                )
        else:
            await app.send_edit("Reply to supported media . . .", delme=3, text_type=["mono"])




@app.on_message(gen(["qc", "qrcode"]))
async def qrcode_handler(_, m):
    """ qrcode handler for image plugin """
    try:
        picname = f"{app.TEMP_DICT}qrcode.jpg"
        img = qrcode.make(m.command[1:])
        img.save(
            picname
        )
        await app.send_edit("Making qrcode . . .", text_type=["mono"])
        await app.send_document(
            m.chat.id,
            picname
        )
        if os.path.exists(picname):
            os.remove(picname)

        await m.delete()
    except Exception as e:
        await app.error(e)




@app.on_message(gen(["colour", "color"]))
async def colourtemplate_handler(_, m: Message):
    """ colourtemplate handler for image plugin """
    if app.long() == 1:
        await app.send_edit("Please give some colour name after command . . .", delme=3)

    elif app.long() > 1:
        if app.textlen() <= 4096:
            try:
                w, h = 60, 30
                if app.long() > 2:
                    args = app.GetArgs().text.split()
                    w, h = args[2], args[3]

                picname = f"{app.TEMP_DICT}colour_image.png"
                img = Image.new(
                    "RGB",
                    (w, h),
                    color = f"{m.command[1]}"
                    )
                img.save(picname)
                await app.send_edit(f"Making {m.command[1]} template . . .", text_type=["mono"])
                await app.send_photo(
                    m.chat.id,
                    picname
                    )
                await m.delete()
                if os.path.exists(picname):
                    os.remove(picname)
            except Exception as e:
                await app.error(e)
        else:
            await app.send_edit("Something went wrong !", text_type=["mono"], delme=3)




@app.on_message(gen("cat"))
async def catpic_handler(_, m):
    try:
        await m.delete()
        data = requests.get("https://api.thecatapi.com/v1/images/search").text
        data = json.loads(data)
        img = data[0]["url"]
        await app.send_photo(m.chat.id, img)
    except Exception as e:
        print(e)
        await app.send_edit("Sorry, No cat pic found !")




@app.on_message(gen("waifu"))
async def waifupic_handler(_, m):
    text = "Finding waifu . . ."
    try:
        if app.long() == 1:
            await app.send_edit(text, text_type=["mono"])
            data = requests.get("https://api.waifu.pics/sfw/waifu")
            photo = data.json().get("url")
            if photo:
                await app.send_photo(m.chat.id, photo)
                await m.delete()
            else:
                await app.send_edit("No waifu found !", delme=3)
        elif app.long() > 1 and m.command[1] == "nsfw":
            await app.send_edit(text, text_type=["mono"])
            data = requests.get("https://api.waifu.pics/nsfw/waifu")
            photo = data.json().get("url")
            if photo:
                await app.send_photo("me", photo)
                await app.send_edit("The pic was sent in your saved message . . .")
            else:
                await app.send_edit("No waifu found !", delme=3)
        elif app.long() > 1 and m.command[1] != "nsfw":
            await app.send_edit(text, text_type=["mono"])
            data = requests.get("https://api.waifu.pics/sfw/waifu")
            photo = data.json().get("url")
            if photo:
                await app.send_photo(m.chat.id, photo)
                await m.delete()
            else:
                await app.send_edit("No waifu found !", delme=3)
    except Exception as e:
        await app.error(e)




@app.on_message(gen("poto"))
async def profilepic_handler(_, m):
    msg = await app.send_edit("Getting profile pic . . .", text_type=["mono"])
    await send_profile_pic(m)
    await msg.delete()




@app.on_message(gen("dog"))
async def dogpic_handler(_, m):
    try:
        img_url = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
        if img_url:
            await app.send_photo(m.chat.id, img_url)
        else:
            await app.send_edit("No dog pics found !", text_type=["mono"])
    except Exception as e:
        await app.send_edit("No dog pics Found !", text_type=["mono"])
        await app.error(e)
