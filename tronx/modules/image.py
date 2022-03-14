import os
import time
import asyncio
import qrcode
import requests
import json

from PIL import Image, ImageOps, ImageDraw, ImageFont

from pyrogram import filters, Client
from pyrogram.errors import UsernameInvalid
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




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
	await app.send_edit(
		m, 
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




async def send_profile_pic(app: Client, m: Message, arg=True, p_id=False):
	reply = m.reply_to_message 
	if not p_id:
		p_id = await app.get_profile_photos(reply.from_user.id)
	photo = []
	photo.clear()
	if not arg:
		for x in p_id:
			await app.send_cached_media(m.chat.id, x["file_id"])
			time.sleep(0.30)
	elif arg:
		for x in p_id:
			photo.append(x["file_id"])
			if len(photo) == 5:
				break
			else:
				pass
		for x in photo:
			await app.send_cached_media(m.chat.id, x)
	else:
		print("failed to send Profile photo")




@app.on_message(gen(["uns", "unsplash"], allow = ["sudo"]))
async def unsplash_handler(_, m: Message):
	cmd = m.command
	if app.long(m) == 1:
		await app.send_edit(m, "Give me some query after command . . .", text_type=["mono"], delme=4)
	elif app.long(m) == 2:
		if cmd[1].isdigit():
			return await app.send_edit(m, "Sorry but give me a text query.", text_type=["mono"], delme=4)
		else:
			keyword = cmd[1]
		await get_image(m, keyword)
	elif app.long(m) > 2:
		images = []
		images.clear()
		if cmd[1].isdigit():
			if app.is_str(cmd[2]):
				m = await app.send_edit(m, "Getting images . . .", text_type=["mono"])
				second = int(cmd[1]) + 1
				keyword = cmd[2]
				for x in range(1, second):
					img = await app.get_url(
						f"https://source.unsplash.com/1600x900/?{keyword}"
						)
					images.append(img)

				m = await app.send_edit(m, "Getting image . . .", text_type=["mono"])
				for img in images:
					await asyncio.gather(
						app.send_photo(m.chat.id, str(img))
						)
				if m.from_user.is_self:
					await m.delete()
			else:
				await app.send_edit(m, "Sorry numbers are not allowed to be a search query.", delme=4, text_type=["mono"])  
		else:
			await app.send_edit(m, "Give me count number of how many images you need.", delme=4, text_type=["mono"])
	else:
		return app.send_edit(m, "Something went wrong !", text_type=["mono"], delme=4)




@app.on_message(gen("stoi", allow = ["sudo"]))
async def stoi_handler(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "reply to a sticker.", text_type=["mono"], delme=3)

	elif reply:
		if reply.sticker:
			if not reply.sticker.is_animated:
				filename = f"{app.TEMP_DICT}sticker.jpg"
				m = await app.send_edit(m, '`Converting To Image...`')
				await app.download_media(
					message=reply, 
					file_name=filename
					)
				await app.send_photo(
					m.chat.id, 
					filename, 
					reply_to_message_id=reply.message_id
					)
				await m.delete()
				if os.path.exists(filename):
					os.remove(filename)
			else:
				await app.send_edit(m, "Animated Stickers are Not Supported!", delme=2, text_type=["mono"])
		else:
			await app.send_edit(m, "Reply to a sticker please !", delme=2, text_type=["mono"])




@app.on_message(gen("itos", allow = ["sudo"]))
async def itos_handler(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Reply to a image.", text_type=["mono"], delme=4)

	elif reply:
		if reply.photo or reply.document.file_name.endswith(".png" or ".jpg" or "jpeg"):
			if not reply.video:
				m = await app.send_edit(m, "Converting To Sticker . . .", text_type=["mono"])
				filename = f"{app.TEMP_DICT}sticker.webp"
				await app.download_media(
					message=reply, 
					file_name=filename
					)
				await app.send_sticker(
					m.chat.id, 
					filename, 
					reply_to_message_id=reply.message_id)
				await m.delete()
				if os.path.exists(filename):
					os.remove(filename)
			else:
				await app.send_edit(m, "video and animated Stickers Not Supported!", delme=3, text_type=["mono"])
		else:
			await app.send_edit(m, "Reply to supported media . . .", delme=3, text_type=["mono"])




@app.on_message(gen(["qc", "qrcode"], allow = ["sudo"]))
async def qrcode_handler(_, m):
		try:
			picname = f"{app.TEMP_DICT}qrcode.jpg"
			img = qrcode.make(m.command[1:])
			img.save(
				picname
				)
			m = await app.send_edit(m, "Making qrcode . . .", text_type=["mono"])
			await app.send_document(
				m.chat.id, 
				picname
				)
			if os.path.exists(picname):
				os.remove(picname)
			await m.delete()
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen(["colour", "color"], allow = ["sudo"]))
async def colourtemplate_handler(_, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Please give some colour name after command . . .", delme=3)

	elif app.long(m) > 1:
		if app.textlen(m) <= 4096:
			try:
				picname = f"{app.TEMP_DICT}colour_image.png"
				img = Image.new(
					"RGB", 
					(60, 30), 
					color = f"{m.command[1]}"
					)
				img.save(picname)
				m = await app.send_edit(m, "Making colour . . .", text_type=["mono"])
				await app.send_photo(
					m.chat.id,
					picname
					)
				await m.delete()
				if os.path.exists(picname):
					os.remove(picname)
			except Exception as e:
				await app.error(m, e)
		else:
			await app.send_edit(m, "Something went wrong !", text_type=["mono"], delme=4)




@app.on_message(gen("cat", allow = ["sudo"]))
async def catpic_handler(_, m):
	try:
		await m.delete()
		data = requests.get("https://api.thecatapi.com/v1/images/search").text
		data = json.loads(data)
		img = data[0]["url"]
		await app.send_photo(m.chat.id, img)
	except Exception as e:
		print(e)
		await app.send_edit(m, "Sorry, No cat pic found !")




@app.on_message(gen("waifu", allow = ["sudo"]))
async def waifupic_handler(_, m):
	text = "Finding waifu . . ."
	try:
		if app.long(m) == 1:
			m = await app.send_edit(m, text, text_type=["mono"])
			data = requests.get(f"https://api.waifu.pics/sfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo(m.chat.id, photo)
				await m.delete()
			else:
				await app.send_edit(m, "No waifu found !", delme=3)
		elif app.long(m) > 1 and m.command[1] == "nsfw":
			m = await app.send_edit(m, text, text_type=["mono"])
			data = requests.get(f"https://api.waifu.pics/nsfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo("me", photo)
				await app.send_edit(m, "The pic was sent in your saved message . . .")
			else:
				await app.send_edit(m, "No waifu found !", delme=3)
		elif app.long(m) > 1 and m.command[1] != "nsfw":
			m = await app.send_edit(m, text, text_type=["mono"])
			data = requests.get(f"https://api.waifu.pics/sfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo(m.chat.id, photo)
				await m.delete()
			else:
				await app.send_edit(m, "No waifu found !", delme=3)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("poto", allow = ["sudo"]))
async def profilepic_handler(_, m):
	reply = m.reply_to_message
	cmd = m.command
	text = "Getting photo . . ."
	oldmsg = m

	if reply:
		try:
			if app.long(m) > 1:
				m = await app.send_edit(m, text, text_type=["mono"])
				if cmd[1] == "all":
					await send_profile_pic(app, m, False)
				if cmd[1] != "all":
					await send_profile_pic(app, m)
				await m.delete()

			if app.long(m) == 1:
				m = await app.send_edit(m, text, text_type=["mono"])
				await send_profile_pic(app, m)
				await m.delete()
		except Exception as e:
			await app.error(m, e)

	elif not reply:
		if app.long(m) > 1:
			try:
				m = await app.send_edit(m, text, text_type=["mono"])
				user = await app.get_users(cmd[1])
				p_id = await app.get_profile_photos(user.id)
				await send_profile_pic(app, m, p_id=p_id)
				await m.delete()
			except UsernameInvalid:
				await app.send_edit(m, "Sorry this username does not exist . . .", text_type=["mono"])

		elif app.long(m) == 1:
			user = m.from_user
			p_id = await app.get_profile_photos(user.id)
			await send_profile_pic(app, m, p_id=p_id)
			await m.delete()
