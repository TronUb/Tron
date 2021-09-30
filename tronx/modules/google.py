import os
import re
import time
import json
import random
import asyncio
import urllib
import requests
import http.cookiejar
from bs4 import BeautifulSoup
from google_images_download import google_images_download

from pyrogram import Client, filters
from pyrogram.types import Message, User

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
	long,
)




CMD_HELP.update(
	{"google" : (
		"google",
		{
		"img [number of pic] [query]" : "Search something on google ans get the photo of that query",
		"sauce [reply to pic]" : "Get the source link of that image",
		"pic [query]" : "Get Images from @bing bot.",
		}
		)
	}
)




search_url = "http://www.google.com"

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
}

def get_soup(url,header):
	return BeautifulSoup(urllib.request.urlopen(urllib.request(url,headers=header)),'html.parser')




@app.on_message(gen("sauce"))
async def image_sauce(_, m: Message):
	try:
		reply = m.reply_to_message
		if reply.photo:
			await send_edit(m, "⏳ • Hold on ...")
			universe = "photo_{}_{}.png".format(
				reply.photo.file_id, 
				reply.photo.date
				)
			await app.download_media(
				reply.photo,
				file_name="tronx/downloads/" + universe
				)
		elif reply.animation:
			await send_edit(m, "⏳ • Hold on ...")
			universe = "giphy_{}-{}.gif".format(
				reply.animation.date,
				reply.animation.file_size
				)
			await app.download_media(
				reply.animation,
				file_name="tronx/downloads/" + universe
				)
		else:
			await send_edit(m, "Only photo & animation media supported.", delme=3)
			return
		searchUrl = 'http://www.google.co.id/searchbyimage/upload'
		filePath = 'tronx/downloads/{}'.format(universe)
		multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
		response = requests.post(searchUrl, files=multipart, allow_redirects=False)
		fetchUrl = response.headers['Location']
		await send_edit(m, "Results: [Tap Here]({})".format(fetchUrl), disable_web_page_preview = True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("pic"))
async def yandex_images(_, m: Message):
	if len(m.text.split()) == 1:
		await send_edit(m, "Usage: `.pic cat`", delme=3)
		return
	try:
		if len(m.text.split()) > 1:
			node = await send_edit(m, "`Getting image ...`")
			photo = m.text.split(None, 1)[1]
			result = await app.get_inline_bot_results(
				"@pic", 
				photo
			)
			await m.delete(node)
			saved = await app.send_inline_bot_result(
				m.chat.id, 
				query_id=result.query_id, 
				result_id=result.results[random.randint(0, len(result.results))].id, 
				hide_via=True
			)
		else:
			await send_edit(m, "Failed to get the image, try again later !", delme=3)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("img"))
async def google_img(_, m: Message):
	if bool(m.command[1].isdigit()):
		images = m.command[1]
		search = m.text.split(None, 2)[2]
	else:
		images = 3
		search = m.text.split(None, 1)[1]
	try:
		await send_edit(m, f"Sending `{search}` images ...")
		response = google_images_download.googleimagesdownload()
		arguments = {"keywords":f"{search}", "limit":f"{images}", "print_urls":True}
		paths = response.download(arguments) # creates directory of searched keyword
		for poto in os.listdir(f"/workspace/downloads/{search}/"):
			if poto.endswith((".jpg", ".png", "jpeg")):
				await app.send_photo(
					m.chat.id, 
					f"/workspace/downloads/{search}/{poto}")
			else:
				await send_edit(
					m, 
					f"[ `/workspace/downloads/{search}/{poto}` ] is not a photo")
			os.remove(
				f"/workspace/downloads/{search}/{poto}" # remove files from folders
			)
		os.rmdir(f"/workspace/downloads/{search}") # remove empty folders
	except Exception as e:
		await error(m, e)