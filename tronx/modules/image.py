import os, time, asyncio, qrcode, requests

from PIL import Image, ImageOps, ImageDraw, ImageFont

from pyrogram import filters, Client
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	# others
	AioHttp,
	long,
)




CMD_HELP.update(
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




@app.on_message(gen("uns"))
async def unsplash(_, m: Message):
	cmd = m.command
	if long(m) > 1 and isinstance(cmd[1], str):
		keyword = cmd[1]
		if long(m) > 2 and int(cmd[2]) < 10:
			await send_edit(m, "`Getting Pictures`")
			count = int(cmd[2])
			images = []
			while len(images) is not count:
				img = await AioHttp().get_url(
					f"https://source.unsplash.com/1600x900/?{keyword}"
				)
				if img not in images:
					images.append(img)
			for img in images:
				await app.send_photo(m.chat.id, str(img))
			await m.delete()
			return
		else:
			await send_edit(
				m, 
				"`Getting Picture`"
				)
			img = await AioHttp().get_url(
				f"https://source.unsplash.com/1600x900/?{keyword}"
			)
			await asyncio.gather(
				m.delete(), 
				app.send_photo(m.chat.id, str(img))
			)




@app.on_message(gen("stoi"))
async def stick2image(_, m):
	if not m.reply_to_message:
		await send_edit(m, "`reply to a sticker . . .`", delme=3)
	elif m.reply_to_message:
		reply = m.reply_to_message
		if reply.sticker:
			if not reply.sticker.is_animated:
				await send_edit(m, '`Converting To Image...`')
				file = await app.download_media(
					message=reply, 
					file_name='Tron/tronx/downloads/test.jpg'
					)
				await app.send_photo(
					m.chat.id, 
					'Tron/tronx/downloads/test.jpg', 
					reply_to_message_id=m.reply_to_message.message_id
					)
				await m.delete()
				os.remove('Tron/tronx/downloads/test.jpg')
			else:
				await m.edit('<b>Animated Stickers are Not Supported!</b>')
				await asyncio.sleep(3)
				await m.delete()    
		else:
			msg = await send_edit(m, '**Reply to a non-animated sticker !**', delme=3)




@app.on_message(gen("itos"))
async def image2stick(app, m):
	if not m.reply_to_message:
		await send_edit(m, "`Reply to a image`", delme=3)
	elif m.reply_to_message:
		reply = m.reply_to_message
		if reply.photo or reply.document.file_name.endswith == ".png" or ".jpg" or "jpeg":
			if not reply.video:
				await m.edit('`Converting To Sticker ...`')
				file = await app.download_media(message=reply, file_name=f"{Config.TEMP_DICT}sticker.webp")
				await app.send_sticker(
					m.chat.id, 
					f"{Config.TEMP_DICT}sticker.webp", 
					reply_to_message_id=m.reply_to_message.message_id)
				await m.delete()
				os.remove(f"{Config.TEMP_DICT}sticker.webp")
			else:
				await send_edit(m, 'video and animated Stickers Not Supported!', delme=3)
				await asyncio.sleep(3)
				await m.delete()    
		else:
			msg = await send_edit(m, '**Reply to supported media ...**', delme=3)




@app.on_message(gen(["qc", "qrcode"]))
async def make_qr(app, m):
		try:
			await send_edit(m, "making qrcode ...")
			img = qrcode.make(m.command[1:])
			alva = img.save(
				f"{Config.TEMP_DICT}qrcode.jpg"
				)
			await app.send_document(
				m.chat.id, 
				f"{Config.TEMP_DICT}qrcode.jpg"
				)
			await m.delete()
		except Exception as e:
			await error(m, e)




@app.on_message(gen("colour"))
async def colour_templates(_, m: Message):
	if len(m.command) < 2:
		await send_edit(m, "Please give some colour name after command ...", delme=3)
	elif len(m.command) > 1:
		if len(m.command) < 4096:
			try:
				await send_edit(m, "creating image ...")
				img = Image.new(
					'RGB', 
					(60, 30), 
					color = f"{m.command[1]}"
					)
				img.save('colour_image.png')
				time.sleep(0.50)
				await app.send_photo(
					m.chat.id,
					"/workspace/colour_image.png"
					)
				await m.delete()
			except Exception as e:
				await error(m, e)
		else:
			await send_edit(m, "Only 4096 charactes are allowed ! ...", delme=3)




@app.on_message(gen("cat"))
async def get_cat_image(_, m):
	try:
		await m.delete()
		if long(m) == 1:
			await app.send_photo(
				m.chat.id, 
				"https://cataas.com/cat"
			)
		elif long(m) > 1 and m.command[1] == "gif":
			await app.send_animation(
				m.chat.id, 
				"https://cataas.com/cat/gif"
			)
		elif long(m) > 1 and m.command[1] != "gif":
			await app.send_photo(
				m.chat.id, 
				"https://cataas.com/cat"
			)
	except Exception as e:
		await print(e)
		await send_edit(m, "Sorry, No cats found !")




@app.on_message(gen("waifu"))
async def insult_someone(_, m):
	try:
		await send_edit(m, "Finding a waifu . . .")
		if long(m) == 1:
			data = requests.get(f"https://api.waifu.pics/sfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo(m.chat.id, photo)
				await m.delete()
			else:
				await send_edit(m, "No waifu found !", delme=3)
		elif long(m) > 1 and m.command[1] == "nsfw":
			data = requests.get(f"https://api.waifu.pics/nsfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo("me", photo)
				await send_edit(m, "The pic was sent in your saved message . . .")
			else:
				await send_edit(m, "No waifu found !", delme=3)
		elif long(m) > 1 and m.command[1] != "nsfw":
			data = requests.get(f"https://api.waifu.pics/sfw/waifu")
			photo = data.json().get("url")
			if photo:
				await app.send_photo(m.chat.id, photo)
				await m.delete()
			else:
				await send_edit(m, "No waifu found !", delme=3)
	except Exception as e:
		await error(m, e)




async def send_profile_pic(app: Client, m: Message, arg=True, p_id=False):
	reply = m.reply_to_message 
	if p_id:
		p_id = p_id
	elif not p_id:
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




@app.on_message(gen("poto"))
async def get_photos(_, m):
	reply = m.reply_to_message
	cmd = m.command
	await send_edit(m, "Sending profile photos . . .")
	if reply:
		try:
			if long(m) > 1:
				if cmd[1] == "all":
					await send_profile_pic(app, m, False)
				if cmd[1] != "all":
					await send_profile_pic(app, m)

			if long(m) == 1:
				await send_profile_pic(app, m)
		except Exception as e:
			await error(m, e)

	elif not reply:
		if long(m) > 1:
			user = await app.get_users(cmd[1])
			p_id = await app.get_profile_photos(user.id)
			await send_profile_pic(app, m, p_id=p_id)

		elif long(m) == 1:
			user = m.from_user
			p_id = await app.get_profile_photos(user.id)
			await send_profile_pic(app, m, p_id=p_id)
	await m.delete()