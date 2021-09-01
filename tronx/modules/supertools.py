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
)




CMD_HELP.update(
	{"supertools" : (
		"supertools",
		{
		"whois [reply to user] or [username]" : "Get a short list of information of a specific user.",
		"id [reply to user] or [username]" : "Get telegram id of a user or a chat.",
		"ud [query]" : "Get The Meaning Of Any Word In Urban Dictionary.",
		"short [link]" : "Shorten a link into da.gd link.",
		"unshort [shortlink]" : "Reverse the da.gd link to real link.",
		"tts [reply to text]" : "Text To Speech, Convert Text Message To Voice | audio (mp3).",
		"wtr [city name]" : "Type Command And Your City Name To Get Weather Details.",
		"ws [site link]" : "Take A Screenshot Of Any Website And Get The Image Of That Site.",
		}
		)
	}
)


weather_lang_code="en"
lang_code = os.getenv("LANG_CODE", "en")


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")



@app.on_message(gen(["tts"]))
async def voice(_, m: Message):
	replied = m.reply_to_message
	if not replied and len(m.command) < 2:
		await send_edit(
			m, 
			"`reply to someone's text message & use only command`"
			)
		time.sleep(2)
		await m.delete()
		return
	elif not replied and len(m.command) > 1:
		try:
			await send_edit(
				m, 
				"`Converting text to voice ...`"
				)
			text = m.text.split(None, 1)[1]
			tts = gTTS(text, lang=lang_code)
			tts.save("tronx/downloads/voice.mp3")
			await app.send_voice(
				m.chat.id, 
				voice="tronx/downloads/voice.mp3", 
				reply_to_message_id=m.message_id
				)
			await m.delete()
			os.remove("tronx/downloads/voice.mp3")
		except Exception as e:
			await error(m, e)
	elif replied:
		try:
			await send_edit(
				m, 
				"`Converting text to voice ...`"
				)
			text = replied.text
			tts = gTTS(text, lang=lang_code)
			tts.save("tronx/downloads/voice.mp3")
			await app.send_voice(
				m.chat.id, 
				voice="tronx/downloads/voice.mp3", 
				reply_to_message_id=replied.message_id
				)
			await m.delete()
			os.remove("tronx/downloads/voice.mp3")
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			"Something went wrong !"
			)




@app.on_message(gen(["ud"]))
async def urban_dictionary(_, m:Message):
	if len(m.text.split()) == 1:
		await send_edit(
			m, 
			f"Use: `{PREFIX}ud cats`"
			)
		return
	try:
		text = m.text.split(None, 1)[1]
		response = await AioHttp().get_json(
			f"http://api.urbandictionary.com/v0/define?term={text}"
		)
		word = response["list"][0]["word"]
		definition = response["list"][0]["definition"]
		example = response["list"][0]["example"]
		resp = (
			f"**Text**: __`{replace_text(word)}`__\n"
			f"**Meaning:**\n`{replace_text(definition)}`\n\n"
			f"**Example:**\n`{replace_text(example)}` "
		)
		await send_edit(m, resp)
	except IndexError:
		await send_edit(
			m, 
			"`No Results Found !`"
			)
		time.sleep(1.50)
		await m.delete()




@app.on_message(gen("short"))
async def short_link(_, m: Message):
	replied = m.reply_to_message
	if replied or not replied and len(m.command) < 2:
		await send_edit(
			m, 
			"Please give me some link or reply to a link"
			)
		return
	if not replied and len(m.command) > 1:
		try:
			text_url = m.text.split(None, 1)[1]
			sample_url = f"https://da.gd/s?url={text_url}"
			response = requests.get(sample_url).text
			if response:
				await send_edit(
					m, 
					f"**Generated Link:**\n\nShorted Link: {response}\nYour Link: {text_url}", 
					disable_web_page_preview=True)
			else:
				await send_edit(
					m, 
					"something is wrong. please try again later."
					)
		except Exception as e:
			await error(m, e)
	elif replied:
		try:
			text_url = replied.text
			sample_url = f"https://da.gd/s?url={text_url}"
			response = requests.get(sample_url).text
			if response:
				await send_edit(
					m, 
					f"**Generated Link:**\n\nShortened Link: {response}\nOriginal Link: {text_url}", 
					disable_web_page_preview=True)
			else:
				await send_edit(
					m, 
					"something is wrong. please try again later."
					)
		except Exception as e:
			await error(m, e)



@app.on_message(gen(["unshort", "noshort"]))
async def unshort_link(_, m: Message):
	replied = m.reply_to_message
	if not replied and len(m.command) < 2:
		await send_edit(
			m, 
			"Please give me a da.gd link to convert to orginal link"
			)
		return
	elif not replied and len(m.command) > 1:
		try:
			text_url = m.text.split(None, 1)[1]
			if not text_url.startswith("https://da.gd/"):
				await send_edit(
					m, 
					"Please Give me a valid link that starts with `https://da.gd/`"
					)
				return
			else:
				r = requests.get(
					text_url, 
					allow_redirects=False
					)
				if str(r.status_code).startswith("3"):
					fakelink = r.headers["Location"]
					await send_edit(
						m, 
					f"**Generated Links:**\n\nUnshorted Link: {fakelink}\nYour Link: {text_url}", 
					disable_web_page_preview=True
					)
				else:
					await send_edit(
						m, 
						"something is wrong. please try again later."
						)
		except Exception as e:
			await error(m, e)
	elif replied:
		try:
			text_url = replied.text
			if not text_url.startswith("https://da.gd/"):
				await send_edit(
					m, 
					"Please Give me a valid link that starts with `https://da.gd/`"
					)
				return
			else:
				r = requests.get(
					text, 
					allow_redirects=False
					)
				if str(r.status_code).startswith("3"):
					fakelink = r.headers["Location"]
					await send_edit(
						m, 
						f"**Generated Links:**\n\nUnshorted Link: {fakelink}\nYour Link: {text_url}", 
						disable_web_page_preview=True
						)
				else:
					await send_edit(
						m,
						"something is wrong. please try again later."
						)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			"Something went wrong, try again later !"
			)




@app.on_message(gen(["wtr", "weather"]))
async def wtr(_, m: Message):
	if len(m.text.split()) == 1:
		await send_edit(
			m, 
			"Piro Master Atleast Give Me Some Location !!"
			)
		return
	await send_edit(
		m, 
		"Checking weather ..."
		)
	location = m.text.split(None, 1)[1]
	h = {'user-agent': 'httpie'}
	a = requests.get(f"https://wttr.in/{location}?mnTC0&lang={weather_lang_code}", headers=h)
	if "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity." in a.text:
		await send_edit(
			m, 
			"Too many requests, try again later !"
			)
		return
	weather = f"__{escape(a.text)}__"
	await send_edit(
		m, 
		weather, 
		parse_mode="markdown"
		)




@app.on_message(gen(['ws', 'webshot']))
async def webshot(_, m: Message):
	try:
		user_link = m.command[1]
		await send_edit(
			m, 
			"`generating pic ...`"
			)
		full_link = f'https://webshot.deam.io/{user_link}/?delay=2000'
		await app.send_document(
			m.chat.id, 
			full_link, 
			caption=f'{user_link}'
			)
		await m.delete()
	except:
		await send_edit(
			m, 
			"Something went wrong ..."
			)
