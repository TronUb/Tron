import io
import os
import time
import random
import asyncio

from sys import platform
from PIL import Image

from pyrogram import emoji
from pyrogram.types import Message
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.errors import YouBlockedUser, StickersetInvalid

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_ID,
	USER_NAME,
	USER_USERNAME
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others 
	get_arg,
)




CMD_HELP.update(
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
async def kang(_, m: Message):
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
				return await send_edit(m, "Sticker has no Name !", mono=True)

			emoji_ = replied.sticker.emoji
			is_anim = replied.sticker.is_animated
			if not replied.sticker.file_name.endswith(".tgs"):
				resize = True
		else:
			return await send_edit(m, "Unsupported File !", mono=True)

		await send_edit(m, f"{random.choice(KANGING_STR)}", mono=True)

		photo = await app.download_media(message=replied)
	else:
		return await send_edit(m, "I can't kang that . . .", mono=True)

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

		if USER_USERNAME:
			u_name = USER_USERNAME
		else:
			u_name = USER_NAME or USER_ID

		packname = f"a{USER_ID}_by_tron_{pack}"
		custom_packnick = f"{u_name}'s kang pack"
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
			exist = await app.send(
				GetStickerSet(stickerset=InputStickerSetShortName(short_name=packname))
			)
		except StickersetInvalid:
			pass
		if exist is not False:
			try:
				await app.send_message("Stickers", "/addsticker")
			except YouBlockedUser:
				return await send_edit(m, "first Unblock @Stickers . . .")

			await asyncio.sleep(0.40)
			await app.send_message("Stickers", packname)
			limit = "50" if is_anim else "120"
			while limit in await get_response(m):
				pack += 1
				packname = f"a{user.id}_by_zect_{pack}"
				packnick = f"{custom_packnick} Vol.{pack}"
				if is_anim:
					packname += "_anim"
					packnick += " (Animated)"
				await send_edit(m, "Switching to Pack " + str(pack) + " due to insufficient space") 

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
						await app.send_message(
							"Stickers", f"<{packnick}>", parse_mode=None
						)
					await asyncio.sleep(0.40)
					await get_response(m)
					await app.send_message("Stickers", "/skip")
					await asyncio.sleep(0.40)
					await get_response(m)
					await app.send_message("Stickers", packname)
					await asyncio.sleep(0.40)
					out = f"[kanged](t.me/addstickers/{packname})"
					await send_edit(m, 
						f"**Sticker** {out} __in a Different Pack__**!**"
					)
					return
			await app.send_document("Stickers", photo)
			time.sleep(0.2)
			await asyncio.sleep(0.40)
			rsp = await get_response(m)
			if "Sorry, the file type is invalid." in rsp:
				return await send_edit(m, "Failed to add sticker, use @Stickers bot to add the sticker manually.", mono=True)

			await app.send_message("Stickers", emoji_)
			await asyncio.sleep(0.40)
			await get_response(m)
			await app.send_message("Stickers", "/done")
		else:
			await send_edit(m, "Brewing a new Pack . . .")
			try:
				await asyncio.sleep(0.40)
				await app.send_message("Stickers", cmd)
			except YouBlockedUser:
				return await send_edit(m, "first **unblock** @Stickers")

			await app.send_message("Stickers", packnick)
			await asyncio.sleep(0.40)
			await get_response(m)
			await app.send_document("Stickers", photo)
			await asyncio.sleep(0.40)
			await get_response(m)
			rsp = await get_response(m)
			if "Sorry, the file type is invalid." in rsp:
				return await send_edit(m, "Failed to add sticker, use @Stickers bot to add the sticker manually.")

			await app.send_message("Stickers", emoji_)
			await asyncio.sleep(0.40)
			await get_response(m)
			await app.send_message("Stickers", "/publish")
			if is_anim:
				await asyncio.sleep(0.40)
				await get_response(m)
				await app.send_message("Stickers", f"<{packnick}>", parse_mode=None)
				await asyncio.sleep(0.40)
			await get_response(m)
			await app.send_message("Stickers", "/skip")
			await asyncio.sleep(0.40)
			await get_response(m)
			await app.send_message("Stickers", packname)
			await asyncio.sleep(0.40)
		await send_edit(m, f"[kanged](t.me/addstickers/{packname})", delme=True)
		await app.read_history("Stickers")
		if os.path.exists(str(photo)):
			os.remove(photo)




@app.on_message(gen("stinfo"))
async def sticker_pack_info_(_, m: Message):
	replied = m.reply_to_message
	if not replied:
		return await send_edit(m, "I can't fetch info from nothing, can I ?!", mono=True)

	if not replied.sticker:
		return await send_edit(m, "Reply to a sticker to get the pack details.", mono=True)

	await send_edit(m, "Fetching details of the sticker pack, please wait . . .", mono=True)
	get_stickerset = await app.send(
		GetStickerSet(
			stickerset=InputStickerSetShortName(short_name=replied.sticker.set_name)
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
	await send_edit(m, out_str)




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
	return [x async for x in app.iter_history("Stickers", limit=1)][0].text




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



