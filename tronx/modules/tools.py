import speedtest

from datetime import datetime

from currency_converter import CurrencyConverter

from pyrogram.types import Message
from pyrogram.errors import (
	MessageTooLong,
)

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"tools" : (
		"tools",
		{
		"wlink" : "Get message links which contain the query word.",
		"cur [10 USD INR]" : "Converts Other Money value In Your Currency value. Just Use The Right Currency Code.",
		"temp [10 c]" : "Get temperature or farenheight, c = celcius, f = farenheight.",
		"json [reply to message]" : "Use This Command To Get Deep Details Of Any Media Or Text.", 
		"ulink [reply to inline button message]" : "Use this to inline or url button message containing links.",
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
	await app.send_edit(m, "Finding word in this chat . . .", mono=True)
	try:
		if app.long(m) < 2:
			return await app.send_edit(m, "Please give some text to search in chat ...")

		else:
			info = await app.get_history(m.chat.id)
			query = m.text.split(None, 1)[1]
			for ele in info:
				msg = str(ele.text)
				if query in msg:
					links.append(f"https://t.me/c/{str(ele.chat.id)[4:]}/{ele.message_id}")
			await app.send_edit(m, "\n".join(links))
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["cur", "currency"]))
async def evaluate(_, m: Message):
	if app.long(m) <= 3:
		return await app.send_edit(m, f"Use | `{app.PREFIX}cur 100 USD INR` or `{app.PREFIX}currency 100 USD INR`")

	value = m.command[1]
	cur1 = m.command[2].upper()
	cur2 = m.command[3].upper()
	try:
		conv = c.convert(int(value), cur1, cur2)
		text = "{} {} = {} {}".format(value, cur1, f'{conv:,.2f}', cur2)
		await app.send_edit(m, text)
	except ValueError as e:
		await app.error(m, e)




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
			await app.send_edit(m, text)
		elif temp2 == "c":
			result = convert_f(temp1)
			text = "`{}°C` = `{}°F`".format(temp1, result)
			await app.send_edit(m, text)
		else:
			await app.send_edit(m, "Unknown type {}".format(temp2))
	except ValueError as e:
		await app.error(m, e)




@app.on_message(gen("json"))
async def json_of_msg(_, m: Message):
	reply = m.reply_to_message

	data = str(reply) if reply else str(m)

	try:
		await app.send_edit(m, data, mono=True)
	except MessageTooLong: # message too long
		await app.send_edit(m, "Sending file . . .", mono=True)
		await app.create_file(m, "json.txt", data)




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
			await app.error(m, e)

		for x in range(len(raw)):
			cat.append(raw[x])

		for y in range(len(cat)):
			dog.append(cat[x][0].url)

		msg = "\n".join(dog)
		if msg:
			await app.send_edit(m, f"`{msg}`")
		else:
			await app.send_edit(m, "There are no links in this message . . .", mono=True)
	else:
		await app.send_edit(m, "Try this command on url button message to get info of the button . . .", mono=True)




@app.on_message(gen("mlink"))
async def get_message_links(_, m: Message):
	reply = m.reply_to_message

	if m.chat.type == "private" or "bot":
		return await app.send_edit(m, "This is not a group, try in groups . . .", delme=2, mono=True)

	elif m.chat.type == "supergroup" or "group":
		if reply:
			try:
				data = await app.get_messages(
					chat_id = m.chat.id, 
					message_ids = reply.message_id
					)
				gid = str(data.chat.id)
				chatid = int(gid.replace("-100", "")) if gid.startswith("-100") else data.chat.id
				msg_id = data.message_id
			except Exception as e:
				await app.error(m, e)
		else:
			try:
				data = await app.get_messages(
					chat_id = m.chat.id,
					message_ids = m.message_id
					)
				gid = str(data.chat.id)
				chatid = int(gid.replace("-100", "")) if gid.startswith("-100") else data.chat.id
				msg_id = data.message_id
			except Exception as e:
				await app.error(m, e)
		try:
			group = await data.username
			await app.send_edit(m, f"https://t.me/{group}/{msg_id}")
		except Exception:
			await app.send_edit(m, f"https://t.me/c/{chatid}/{msg_id}")




@app.on_message(gen("saved"))
async def save_to_cloud(_, m: Message):
	await m.delete()
	await m.reply_to_message.forward("self")




@app.on_message(gen(["fwd", "frwd"]))
async def forward_msgs(_, m: Message):
	reply = m.reply_to_message
	try:
		await m.delete()
		if reply and app.long(m) == 1:
			await reply.forward(m.chat.id)

		elif reply and app.long(m) > 1:
			await reply.forward(m.command[1])

		elif not reply and app.long(m) == 1:
			await m.forward(m.chat.id)

		elif not reply and app.long(m) > 1:
			await app.send_edit(m, "Sir reply to yours or someone's message.", mono=True, delme=3)

		else:
			await app.send_edit(m, "Something went wrong, please try again later !", mono=True, delme=3)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["spt", "speed", "speedtest"]))
async def speed_tests(app, m: Message):
	if app.long(m) == 1:
		await app.send_edit(m, "Testing speed . . .", mono=True)
		test = speedtest.Speedtest()
		test.get_best_server()
		test.download()
		test.upload()
		test.results.share()
		result = test.results.dict()
		teks = "**⧓ Speed Test Results ⧓**\n\n"
		teks += "**DOWNLOAD ⊢** `{}`\n".format(app.SpeedConvert(result['download']))
		teks += "**UPLOAD ⊢** `{}`\n".format(app.SpeedConvert(result['upload']))
		teks += "**PING ⊢** `{} ms`\n".format(result['ping'])
		teks += "**SERVER ⊢** `{}`\n".format(result['client']['isp'])
		teks += "**LOCATION ⊢** `{}, {}`".format(result['server']['name'], result['server']['country'])
		if teks:
			await app.send_edit(m, teks)
		else:
			await app.send_edit(m, "Something went wrong !", mono=True, delme=5)
	elif app.long(m) > 1 and "pic" in m.command[1]:
		msg = await app.send_edit(m, "Calculating Speed . . .")

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
			await msg.delete()
		else:
			await app.send_edit(m, "Something went wrong !", mono=True, delme=5)





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

			await app.send_edit(m, f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "".join(collect))
		else:
			await app.send_edit(m, "Please reply to someone . . .", mono=True, delme=3)
	except Exception as e:
		await app.error(m, e)


