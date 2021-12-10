import os
import time
import re
import requests

from gtts import gTTS
from html import escape
from asyncio import sleep

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
	create_file,
)




CMD_HELP.update(
	{"supertools" : (
		"supertools",
		{
		"id [reply to user] or [username]" : "Get telegram id of a user or a chat.",
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
	return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


async def text_to_voice(m: Message, text):
	tts = gTTS(text, lang=lang_code)
	tts.save(f"{Config.TEMP_DICT}voice.mp3")
	await app.send_voice(
		m.chat.id, 
		voice=f"{Config.TEMP_DICT}voice.mp3", 
		reply_to_message_id=m.message_id
		)
	await m.delete()
	os.remove(f"{Config.TEMP_DICT}voice.mp3")
	return




async def shorten_link(m: Message, text):
	sample_url = f"https://da.gd/s?url={text}"
	response = requests.get(sample_url).text
	if response:
		await send_edit(
			m, 
			f"**Generated Link:**\n\nShorted Link: {response}\nYour Link: {text}", 
			disable_web_page_preview=True)
	else:
		await send_edit(m, "something is wrong. please try again later.", mono=True)




async def unshorten_link(m: Message, text):
		if not text_url.startswith("https://da.gd/"):
				await send_edit(m, "Please Give me a valid link that starts with `https://da.gd/`")
		else:
			r = requests.get(
				text, 
				allow_redirects=False
			)
			if str(r.status_code).startswith("3"):
				fakelink = r.headers["Location"]
				await send_edit(
					m, 
					f"**Generated Links:**\n\nUnshorted Link: {fakelink}\nYour Link: {text}", 
					disable_web_page_preview=True
				)
			else:
				await send_edit(m,"Something went wrong, please try again later . . .", mono=True)




@app.on_message(gen("tts"))
async def create_voice(_, m: Message):
	reply = m.reply_to_message

	try:
		if not reply and long(m) == 1:
			return await send_edit(m, "Reply to someone's text message or give me the text as a suffix . . .", delme=True, mono=True)

		elif not reply and long(m) > 1:
			await send_edit(m, "Converting text to voice . . .", mono=True)
			text = m.text.split(None, 1)[1]
			await text_to_voice(m, text)

		elif reply:
			if not reply.text:
				return await send_edit(m, "Please reply to a text . . .", mono=True, delme=3)
			await send_edit(m, "Converting text to voice . . .", mono=True)
			text = reply.text
			await text_to_voice(m, text)

		else:
			await send_edit(m, "Something went wrong !", mono=True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("ud"))
async def urban_dictionary(_, m:Message):
	if long(m) == 1:
		return await send_edit(m, f"Use: `{PREFIX}ud cats`")

	try:
		await send_edit(m, f"Searching for `{m.text.split(None, 1)[1]}`")
		text = m.text.split(None, 1)[1]
		response = await AioHttp().get_json(
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
		await send_edit(m, resp)
	except IndexError:
		await send_edit(m, "No Results Found !", mono=True, delme=3)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("short"))
async def shorten_the_link(_, m: Message):
	reply = m.reply_to_message
	try:
		if not reply and long(m) == 1:
			return await send_edit(m, "Please give me some link or reply to a link", mono=True)

		if not reply and long(m) > 1:
			text = m.text.split(None, 1)[1]
			await shorten_link(m, text)
		elif reply:
			if not reply.text:
				return await send_edit(m, "Please reply to text . . .", mono=True)
			text = reply.text
			await shorten_link(m, text)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["unshort", "noshort"]))
async def unshort_link(_, m: Message):
	reply = m.reply_to_message
	try:
		if not reply and long(m) == 1:
			return await send_edit(m, "Please give me a da.gd link to convert to orginal link", mono=True)

		elif not reply and long(m) > 1:
			text = m.text.split(None, 1)[1]
			await unshorten_link(m, text)

		elif reply:
			if not reply.text:
				return await send_edit(m, "Please reply to a text . . .", mono=True)
			text = reply.text
			await unshorten_link(m, text)

		else:
			await send_edit(m, "Something went wrong, try again later !", mono=True)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["wtr", "weather"]))
async def wtr(_, m: Message):
	if long(m) == 1:
		return await send_edit(m, "Piro Master Atleast Give Me Some Location !", mono=True)

	await send_edit(m, "Checking weather . . .", mono=True)
	location = m.command[1]
	h = {'user-agent': 'httpie'}
	response = requests.get(f"https://wttr.in/{location}?mnTC0&lang={weather_lang_code}", headers=h)
	if "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity." in response.text:
		return await send_edit(m, "Too many requests, try again later !", mono=True)

	weather = f"__{escape(a.text)}__"
	await send_edit(m, weather)




@app.on_message(gen(['ws', 'webshot']))
async def webshot(_, m: Message):
	if long(m) > 1:
		try:
			BASE = "https://render-tron.appspot.com/screenshot/"
			url = m.command[1] 
			path = "downloads/screenshot.jpg"
			response = requests.get(BASE + url, stream=True)

			if response.status_code == 200:
				with open(path, "wb") as file:
					for chunk in response:
						file.write(chunk)
			await send_edit(m, "generating pic . . .", mono=True)
			await app.send_document(
				m.chat.id, 
				path, 
				caption=url
				)
			await m.delete()
			os.remove(path)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Give me the link pro . . .", mono=True)




@app.on_message(gen("undlt"))
async def undelete_msg(_, m: Message):
	collect = []
	collect.clear()
	if long(m) == 1:
		count = 5
	elif long(m) > 1:
		count = m.command[1]
		if not count.isdigit():
			count = 5
	try:
		async for x in app.iter_history(m.chat.id, limit=count):
			if x.text:
				collect.append(f"**Message:** `{x.text}`\n\n")
		await app.send_edit(m, "".join(collect))
	except Exception as e:
		await error(m, e)


