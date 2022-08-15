""" stickers plugin """

import io
import os
import time
import random
import asyncio

from PIL import Image

from pyrogram import emoji
from pyrogram.types import Message
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.errors import YouBlockedUser, StickersetInvalid

from main import app, gen




app.CMD_HELP.update(
    {"stickers" : (
        "stickers",
        {
        "kang [reply to sticker]" : "Adds sticker to your pack or creates new sticker pack.",
        "stinfo [ reply to sticker ]" : "Get sticker pack info."
        }
        )
    }
)




@app.on_message(gen("kang"))
async def kang_handler(_, m: Message):
    """ kang handler for stickers plugin """
    replied = m.reply_to_message
    photo = None
    emoji_ = None
    is_anim = False
    resize = False

    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                return await app.send_edit("Sticker has no Name !", text_type=["mono"])

            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            if not replied.sticker.file_name.endswith(".tgs"):
                resize = True
        else:
            return await app.send_edit("Unsupported File !", text_type=["mono"])

        await app.send_edit(f"{random.choice(KANGING_STR)}", text_type=["mono"])

        photo = await app.download_media(message=replied)
    else:
        return await app.send_edit("I can't kang that . . .", text_type=["mono"])

    if photo:
        args = m.command
        pack = 1
        if len(args) == 2:
            emoji_, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                emoji_ = args[0]

        if emoji_ and emoji_ not in (
            getattr(emoji, a) for a in dir(emoji) if not a.startswith("_")
        ):
            emoji_ = None
        if not emoji_:
            emoji_ = "😐"

        packname = f"a{app.id}_by_tron_{pack}"
        custom_packnick = f"{app.username}'s kang pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        if resize:
            photo = resize_photo(photo)
        if is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"
        exist = False
        try:
            exist = await app.invoke(
                GetStickerSet(stickerset=InputStickerSetShortName(short_name=packname), hash=0)
            )
        except StickersetInvalid:
            pass
        if exist is not False:
            try:
                await app.send_message("Stickers", "/addsticker")
            except YouBlockedUser:
                return await app.send_edit("first Unblock @Stickers . . .")

            await asyncio.sleep(0.40)
            await app.send_message("Stickers", packname)
            limit = "50" if is_anim else "120"
            while limit in await get_response(m):
                pack += 1
                packname = f"a{m.from_user.id}_by_tronub_{pack}"
                packnick = f"{custom_packnick} Vol.{pack}"
                if is_anim:
                    packname += "_anim"
                    packnick += " (Animated)"
                await app.send_edit(
                    "Switching to Pack " + str(pack) + " due to insufficient space"
                )

                await app.send_message("Stickers", packname)
                if await get_response(m) == "Invalid pack selected":
                    await asyncio.sleep(0.40)
                    await app.send_message("Stickers", cmd)
                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_message("Stickers", packnick)
                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_document("Stickers", photo)
                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_message("Stickers", emoji_)
                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_message("Stickers", "/publish")
                    await asyncio.sleep(0.40)
                    if is_anim:
                        await asyncio.sleep(0.40)
                        await get_response(m)
                        await app.send_message("Stickers", f"<{packnick}>")

                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_message("Stickers", "/skip")
                    await asyncio.sleep(0.40)
                    await get_response(m)
                    await app.send_message("Stickers", packname)
                    await asyncio.sleep(0.40)
                    out = f"[kanged](t.me/addstickers/{packname})"
                    await app.send_edit(f"**Sticker** {out} __in a Different Pack__**!**"
                    )
                    return
            await app.send_document("Stickers", photo)
            time.sleep(0.2)
            await asyncio.sleep(0.40)
            rsp = await get_response(m)
            if "Sorry, the file type is invalid." in rsp:
                return await app.send_edit(
                    "Failed to add sticker, use @Stickers bot to add the sticker manually.",
                    text_type=["mono"]
                )

            await app.send_message("Stickers", emoji_)
            await asyncio.sleep(0.40)
            await get_response(m)
            await app.send_message("Stickers", "/done")
        else:
            await app.send_edit("Brewing a new Pack . . .")
            try:
                await asyncio.sleep(0.40)
                await app.send_message("Stickers", cmd)
            except YouBlockedUser:
                return await app.send_edit("first unblock @Stickers.")

            await app.send_message("Stickers", packnick)
            await asyncio.sleep(0.40)
            await get_response(m)
            await app.send_document("Stickers", photo)
            await asyncio.sleep(0.40)
            await get_response(m)
            rsp = await get_response(m)
            if "Sorry, the file type is invalid." in rsp:
                return await app.send_edit(
                    "Failed to add sticker, use @Stickers bot to add the sticker manually."
                )

            await app.send_message("Stickers", emoji_)
            await asyncio.sleep(0.40)
            await get_response(m)
            await app.send_message("Stickers", "/publish")
            if is_anim:
                await asyncio.sleep(0.40)
                await get_response(m)
                await app.send_message("Stickers", f"<{packnick}>")
                await asyncio.sleep(0.40)
            await get_response(m)
            await app.send_message("Stickers", "/skip")
            await asyncio.sleep(0.40)
            await get_response(m)
            await app.send_message("Stickers", packname)
            await asyncio.sleep(0.40)
        await app.send_edit(f"Sticker [kanged](t.me/addstickers/{packname})", delme=True)
        await app.read_history("Stickers")
        if os.path.exists(str(photo)):
            os.remove(photo)




@app.on_message(gen("stinfo"))
async def stinfo_handler(_, m: Message):
    """ stickerinfo handler for stickers plugin """
    replied = m.reply_to_message
    if not replied:
        return await app.send_edit("I can't fetch info from nothing, can I ?!", text_type=["mono"])

    if not replied.sticker:
        return await app.send_edit(
            "Reply to a sticker to get the pack details.",
            text_type=["mono"]
        )

    await app.send_edit(
        "Fetching details of the sticker pack, please wait . . .",
        text_type=["mono"]
    )
    get_stickerset = await app.invoke(
        GetStickerSet(
            stickerset=InputStickerSetShortName(short_name=replied.sticker.set_name),
            hash=0
        )
    )
    pack_emojis = []
    pack_emojis.clear()
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    out_str = (
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Masks:** `{get_stickerset.set.masks}`\n"
        f"**Animated:** `{get_stickerset.set.animated}`\n"
        f"**Stickers In Pack:** `{get_stickerset.set.count}`\n"
        f"**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )
    await app.send_edit(out_str)




def resize_photo(photo: str) -> io.BytesIO:
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))
    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = io.BytesIO()
    resized_photo.name = "sticker.png"
    image.save(resized_photo, "PNG")
    os.remove(photo)
    return resized_photo




async def get_response(m):
    """ get response function for stickers plugin """
    return [x async for x in app.get_chat_history("Stickers", limit=1)][0].text




KANGING_STR = (
    "Stealing in progress ...",
    "Using Dark Power To Kang This Sticker...",
    "Stealing Sticker...",
    "Adding This Sticker To My Pack...",
    "Kanging this sticker...",
    "Noooo, Thet's Ma Stkr\ngib me bck!!!..",
    "Bobi!!! I Stole His Gf\nmuwahhh.",
    "Dem I Lub Dis Stkr ☉｡☉\nLet me kang this...",
    "Arresting This Sticker...",
    "Me Piro Steel Ur Stkr, Hehehe... "
)
