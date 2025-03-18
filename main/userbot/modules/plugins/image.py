""" image plugin """

import os
import asyncio
import qrcode

from PIL import Image

from pyrogram.types import Message

from main import app


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


async def send_profile_pic(m):
    """ sendprofilepic function for image plugin """
    reply = m.reply_to_message
    ids = reply.from_user.id if reply else "me"

    async for x in app.get_chat_photos(ids):
        await app.send_cached_media(m.chat.id, x.file_id)


@app.on_cmd(
    commands="stoi",
    usage="Convert sticker to image."
)
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


@app.on_cmd(
    commands="itos",
    usage="Convert image to sticker."
)
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


@app.on_cmd(
    commands=["qc", "qrcode"],
    usage="Create qr codes of your texts."
)
async def qrcode_handler(_, m):
    """ qrcode handler for image plugin """
    try:
        picname = f"{app.TEMP_DICT}qrcode.jpg"
        img = qrcode.make(m.command[1:])
        img.save(
            picname
        )
        await app.send_edit("Making qrcode . . .", text_type=["mono"])
        await app.send_photo(m.chat.id, picname)
        if os.path.exists(picname):
            os.remove(picname)

        await m.delete()
    except Exception as e:
        await log_error(e)


@app.on_cmd(
    commands=["colour", "color"],
    usage="Create color template images."
)
async def colourtemplate_handler(_, m: Message):
    """ colourtemplate handler for image plugin """
    if app.command() == 1:
        await app.send_edit("Usage: .colour red", delme=3)

    elif app.command() > 1:
        if not app.textlen() > 4096:
            await app.send_edit("Just give me the color name after command ...", text_type=["mono"], delme=3)

        try:
            await app.send_edit(f"Making {m.command[1]} template . . .", text_type=["mono"])
            w, h = 60, 30
            if app.command() > 2:
                args = app.GetArgs().text.split()
                w, h = args[2], args[3]

            picname = f"{app.TEMP_DICT}colour_image.png"
            img = Image.new(
                "RGB",
                (w, h),
                color=f"{m.command[1]}"
            )
            img.save(picname)

            await app.send_photo(
                m.chat.id,
                picname
            )
            await m.delete()
            if os.path.exists(picname):
                os.remove(picname)
        except Exception as e:
            await log_error(e)


@app.on_cmd(
    commands="cat",
    usage="Get cat images."
)
async def catpic_handler(_, m):
    """Fetch and send a random cat image."""
    try:
        # Delete command message (if bot has permission)
        try:
            await m.delete()
        except Exception:
            pass  # Ignore if deletion fails

        # Fetch cat image
        response = await app.fetch_url("https://api.thecatapi.com/v1/images/search")

        if response and response.get("status") == 200:
            cat_data = response.get("data", [])
            cat_img = cat_data[0].get("url") if cat_data else None

            if cat_img:
                await app.send_photo(m.chat.id, cat_img)
            else:
                await app.send_edit("Sorry, No cat pic found!", delme=3)
        else:
            await app.send_edit("Failed to fetch cat image. Try again later!", delme=3)

    except Exception as e:
        await app.send_edit("Error fetching cat image. Try again later!", delme=3)
        await log_error(f"Cat API error: {str(e)}")


@app.on_cmd(
    commands="waifu",
    usage="Get waifu images."
)
async def waifupic_handler(_, m):
    """Fetch and send a random waifu image."""
    try:
        url = "https://api.waifu.pics/sfw/waifu"

        # Check if the command has an argument (for NSFW mode)
        if len(m.command) > 1 and m.command[1].lower() == "nsfw":
            url = "https://api.waifu.pics/nsfw/waifu"

        await app.send_edit("Finding waifu . . .", text_type=["mono"])

        # Fetch waifu image
        response = await app.fetch_url(url)

        if response and response.get("status") == 200:
            photo_url = response.get("data", {}).get("url")

            if photo_url:
                if "nsfw" in url:
                    await app.send_photo("me", photo_url)
                    await app.send_edit("The pic was sent to your saved messages.")
                else:
                    await app.send_photo(m.chat.id, photo_url)
                    await m.delete()
            else:
                await app.send_edit("No waifu found!", delme=3)
        else:
            await app.send_edit(
                "Failed to fetch waifu image. Try again later!", delme=3
            )

    except Exception as e:
        await app.send_edit("Error fetching waifu image. Try again later!", delme=3)
        await log_error(f"Waifu API error: {str(e)}")


@app.on_cmd(
    commands="dog",
    usage="Get dog images."
)
async def dogpic_handler(_, m):
    """Fetch and send a random dog image."""
    try:
        response = await app.fetch_url("https://dog.ceo/api/breeds/image/random")

        if response and response.get("status") == 200:
            img_url = response.get("data", {}).get("message")

            if img_url:
                await app.send_photo(m.chat.id, img_url)
            else:
                await app.send_edit("No dog pics found!", text_type=["mono"], delme=3)
        else:
            await app.send_edit(
                "Failed to fetch dog image. Try again later!",
                text_type=["mono"],
                delme=3,
            )

    except Exception as e:
        await app.send_edit(
            "Error fetching dog image. Try again later!", text_type=["mono"], delme=3
        )
        await log_error(f"Dog API error: {str(e)}")
