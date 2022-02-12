import os
import re
import time
import json
import random
import asyncio
import shutil
import urllib
import requests
import http.cookiejar

from bs4 import BeautifulSoup
from bing_image_downloader import downloader as bing_downloader
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"google" : (
		"google",
		{
		"img [number of pic] [query]" : "uploads searched images on telegram using bing.com",
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
			await app.send_edit(m, "⏳ • Hold on ...")
			universe = "photo_{}_{}.png".format(
				reply.photo.file_id, 
				reply.photo.date
				)
			await app.download_media(
				reply.photo,
				file_name="./downloads/" + universe
				)
		elif reply.animation:
			await app.send_edit(m, "⏳ • Hold on ...")
			universe = "giphy_{}-{}.gif".format(
				reply.animation.date,
				reply.animation.file_size
				)
			await app.download_media(
				reply.animation,
				file_name="./downloads/" + universe
				)
		else:
			return await app.send_edit(m, "Only photo & animation media supported.", delme=3)
		searchUrl = 'http://www.google.co.id/searchbyimage/upload'
		filePath = './downloads/{}'.format(universe)
		multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
		response = requests.post(searchUrl, files=multipart, allow_redirects=False)
		fetchUrl = response.headers['Location']
		await app.send_edit(m, "Results: [Tap Here]({})".format(fetchUrl), disable_web_page_preview = True)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("pic"))
async def yandex_images(_, m: Message):
	if len(m.text.split()) == 1:
		await app.send_edit(m, "Usage: `.pic cat`", delme=3)
		return
	try:
		if len(m.text.split()) > 1:
			node = await app.send_edit(m, "`Getting image ...`")
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
			await app.send_edit(m, "Failed to get the image, try again later !", delme=3)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("img"))
async def image_search(_, m: Message):
	if app.long(m) > 2 and bool(m.command[1].isdigit()):
		limit = m.command[1]
		query = m.text.split(None, 2)[2]
	else:
		limit = 3 # default
		query = m.text.split(None, 1)[1]
	try:
		m = await send_edit(m, f"**Getting images:** `{query}`")
		bing_downloader.download(query, limit=limit,  output_dir="images", adult_filter_off=True, force_replace=True, timeout=60, verbose=False)

		for img in os.listdir(f"./images/{query}"):
			await app.send_photo(m.chat.id, f"./images/{query}/{img}")

		if os.path.exists(f"./images/{query}/"):
			shutil.rmtree(f"./images")

		await m.delete()

	except Exception as e:
		await app.error(m, e)


