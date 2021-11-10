import os
import sys
import time
import ftplib
import requests
import speedtest
import traceback

from datetime import datetime

from io import BytesIO
from currency_converter import CurrencyConverter

from pyrogram import filters, __version__, client
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
	mymention,
	send_edit,
	# others 
	clear_string, 
	speed_convert,
)




CMD_HELP.update(
	{"tools" : (
		"tools",
		{
		"wlink" : "Get message links which contain the query word.",
		"cur [10 USD INR]" : "Converts Other Money value In Your Currency value. Just Use The Right Currency Code.",
		"temp [10 c]" : "Get temperature or farenheight, c = celcius, f = farenheight.",
		"json [reply to message]" : "Use This Command To Get Deep Details Of Any Media Or Text.", 
		"ilink [reply to inline button message]" : "Use this to inline or url button message containing links.",
		"mlink [reply to message]" : "Use this to get message links. both private and public groups.",
		"saved [reply to message]" : "Save Media To Your Telegram Cloud Storage \ Saved Messages.",
		"fwd [reply to message]" : "Forward messages to same group or other groups.",
		"spt" : "Check Hosted Server Speed, use [pic] after command to get image of speedtest.",
		"cchats" : "Get common chats to the replied user."
		}
		)
	}
)




c = CurrencyConverter()


# For converting
def convert_f(fahrenheit):
	f = float(fahrenheit)
	f = (f*9/5)+32
	return(f)


def convert_c(celsius):
	c = float(celsius)
	c = (c-32)*5/9
	return(c)




@app.on_message(gen("wlink"))
async def get_word_links(_, m: Message):
	links = []
	links.clear()
	await send_edit(m, "Finding word in this chat . . .", mono=True)
	try:
		if len(m.command) < 2:
			return await send_edit(m, "Please give some text to search in chat ...")

		else:
			info = await app.get_history(m.chat.id)
			query = m.text.split(None, 1)[1]
			for ele in info:
				msg = str(ele.text)
				if query in msg:
					links.append(f"https://t.me/c/{str(ele.chat.id)[4:]}/{ele.message_id}")
			await send_edit(m, "\n".join(links))
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["cur", "currency"]))
async def evaluate(_, m: Message):
	if len(m.text.split()) <= 3:
		return await send_edit(m, f"Use | `{PREFIX}cur 100 USD INR` or `{PREFIX}currency 100 USD INR`")

	value = m.text.split(None, 3)[1]
	cur1 = m.text.split(None, 3)[2].upper()
	cur2 = m.text.split(None, 3)[3].upper()
	try:
		conv = c.convert(int(value), cur1, cur2)
		text = "{} {} = {} {}".format(value, cur1, f'{conv:,.2f}', cur2)
		await send_edit(m, text)
	except ValueError as e:
		await error(m, e)




@app.on_message(gen(["temp", "temperature"]))
async def evaluate(_, m: Message):
	if len(m.text.split()) <= 2:
		return await send(m, "How To Use: [INSTANT VIEW](https://telegra.ph/HOW-TO-USE-04-11)",disable_web_page_preview=True)

	temp1 = m.text.split(None, 2)[1]
	temp2 = m.text.split(None, 2)[2]
	try:
		if temp2 == "f":
			result = convert_c(temp1)
			text = "`{}°F` = `{}°C`".format(temp1, result)
			await send_edit(m, text)
		elif temp2 == "c":
			result = convert_f(temp1)
			text = "`{}°C` = `{}°F`".format(temp1, result)
			await send_edit(m, text)
		else:
			await send_edit(m, "Unknown type {}".format(temp2))
	except ValueError as e:
		await error(m, e)




@app.on_message(gen("json"))
async def jsonify(app, m: Message):
	reply = m.reply_to_message

	if reply:
		data = reply
	else:
		data = m

	try:
		await send_edit(m, f"{name}")
	except Exception: # message too long
		await send_edit(m, "Sending file . . .", mono=True)

		file = "json.txt"
		new = open(file, "w+")
		new.write(str(data))
		new.close()
		await app.send_document(
			m.chat.id,
			file,
			caption=f"Uploaded By: {mymention()}"
			)
		await m.delete()
		os.remove(file)




@app.on_message(gen("ulink"))
async def get_inlinelinks(app, m: Message):
	reply = m.reply_to_message
	cat = []
	dog = []
	cat.clear()
	dog.clear()

	if reply:
		try:
			raw = reply.reply_markup.inline_keyboard
		except Exception as e:
			await error(m, e)

		for x in range(len(raw)):
			cat.append(raw[x])

		for y in range(len(cat)):
			dog.append(cat[x][0].url)

		msg = "\n".join(dog)
		if msg:
			await send_edit(m, f"`{msg}`")
		else:
			await send_edit(m, "There are no links in this message . . .", mono=True)
	else:
		await send_edit(m, "Try this command on url button message to get info of the button . . .", mono=True)




@app.on_message(gen("mlink"))
async def get_messagelinks(app, m: Message):
	reply = m.reply_to_message

	if m.chat.type == "private" or "bot":
		return await send_edit(m, "This is not a group, try in groups . . .", delme=2, mono=True)

	elif m.chat.type == "supergroup":
		if reply:
			try:
				data = await app.get_messages(
					chat_id = m.chat.id, 
					message_ids = reply.message_id
					)
				gid = str(data.chat.id)
				if gid.startswith("-100"):
					chatid = int(gid.replace("-100", ""))
				else:
					chatid = data.chat.id
				msg_id = data.message_id
			except Exception as e:
				await error(m, e)
		else:
			try:
				data = await app.get_messages(
					chat_id = m.chat.id,
					message_ids = m.message_id
					)
				gid = str(data.chat.id)
				if gid.startswith("-100"):
					chatid = int(gid.replace("-100", ""))
				else:
					chatid = data.chat.id
				msg_id = data.message_id
			except Exception as e:
				await error(m, e)
		try:
			group = await data.username
			await send_edit(m, f"https://t.me/{group}/{msg_id}")
		except Exception:
			await send_edit(m, f"https://t.me/c/{chatid}/{msg_id}")




@app.on_message(gen("saved"))
async def to_saved(_, m: Message):
	await m.delete()
	await m.reply_to_message.forward("self")




@app.on_message(gen("fwd"))
async def to_saved(_, m: Message):
	reply = m.reply_to_message
	try:
		await m.delete()
		if not reply:
			await m.forward(
				m.chat.id
				)
		elif reply and len(m.command) < 2:
			await reply.forward(
				m.chat.id
				)
		elif reply and len(m.command) > 1:
			await reply.forward(
				m.command[1]
				)
	except Exception as e:
		await error(m, e)




@app.on_message(gen(["spt", "speed", "speedtest"]))
async def sptdel(app, m: Message):
	if len(m.command) == 1:
		await send_edit(m, "Testing speed . . .", mono=True)
		test = speedtest.Speedtest()
		test.get_best_server()
		test.download()
		test.upload()
		test.results.share()
		result = test.results.dict()
		teks = "**⧓ Speed Test Results ⧓**\n\n"
		teks += "**DOWNLOAD ⊢** `{}`\n".format(speed_convert(result['download']))
		teks += "**UPLOAD ⊢** `{}`\n".format(speed_convert(result['upload']))
		teks += "**PING ⊢** `{} ms`\n".format(result['ping'])
		teks += "**SERVER ⊢** `{}`\n".format(result['client']['isp'])
		teks += "**LOCATION ⊢** `{}, {}`".format(result['server']['name'], result['server']['country'])
		if teks:
			await send_edit(m, teks)
		else:
			await send_edit(m, "Something went wrong !!")
	elif long(m) > 1 and "pic" in m.command[1]:
		await send_edit(m, "Calculating Speed . . .")

		start = datetime.now()
		s = speedtest.Speedtest()
		s.get_best_server()
		s.download()
		s.upload()
		end = datetime.now()
		ms = (end - start).microseconds / 1000
		response = s.results.dict()
		download = response.get("download")
		upload = response.get("upload")
		ping = response.get("ping")
		agent = response.get("client")
		isp = agent.get("isp")
		isp_rating = agent.get("isprating")
		response = s.results.share()
		speedtest_image = response
		if speedtest_image:
			await app.send_photo(
				m.chat.id,
				speedtest_image,
				caption="**Time Taken:** {} ms".format(ms),
				parse_mode="markdown"
			)
			await m.delete()
		else:
			await send_edit(m, "Something went wrong !", mono=True)





@app.on_message(gen(["cc", "cchats"]))
async def common_chats(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			collect = []
			collect.clear()
			data = await app.get_common_chats(reply.from_user.id)
			for x in data:
				collect.append(x["title"] + "\n")

			await send_edit(m, f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "".join(collect))
		else:
			await send_edit(m, "Please reply to someone . . .", mono=True, delme=3)
	except Exception as e:
		await error(m, e)


