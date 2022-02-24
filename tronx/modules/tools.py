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




@app.on_message(gen("wlink", allow = ["sudo", "channel"]))
async def get_word_links(_, m: Message):
	links = []
	links.clear()

	try:
		if app.long(m) == 2:
			return await app.send_edit(m, "Please give some text to search in chat ...")

		else:
			m = await app.send_edit(m, "Finding word in this chat . . .", mono=True)
			info = await app.get_history(m.chat.id)
			query = m.text.split(None, 1)[1]
			for words in info:
				if query in words:
					links.append(words)

			await app.send_edit(m, f"**FOUND LINKS FOR:** `{query}`\n\n" +"\n".join(links))
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["cur", "currency"], allow = ["sudo", "channel"]))
async def evaluate(_, m: Message):
	if app.long(m) <= 3:
		return await app.send_edit(m, f"Use | `{app.PREFIX}cur 100 USD INR` or `{app.PREFIX}currency 100 USD INR`")

	value = m.command[1]
	cur1 = m.command[2].upper()
	cur2 = m.command[3].upper()
	try:
		m = await app.send_edit(m, f"Converting from `{cur1}` to `{cur2}` . . .")
		conv = c.convert(int(value), cur1, cur2)
		text = f"`{value}` `{cur1}` = `{conv:,.2f}` `{cur2}`"
		await app.send_edit(m, text)
	except ValueError as e:
		await app.error(m, e)




@app.on_message(gen(["temp", "temperature"], allow = ["sudo", "channel"]))
async def evaluate(_, m: Message):
	if app.long(m) <= 2:
		return await app.send_edit(m, "How To Use: [INSTANT VIEW](https://telegra.ph/HOW-TO-USE-04-11)", disable_web_page_preview=True)

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
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("json", allow = ["sudo", "channel", "forward"]))
async def json_of_msg(_, m: Message):
	reply = m.reply_to_message

	data = str(reply) if reply else str(m)

	try:
		await app.send_edit(m, data, mono=True)
	except Exception: # message too long
		m = await app.send_edit(m, "Sending file . . .", mono=True)
		await app.create_file(m, "json.txt", data)
		if m.from_user.is_self:
			await m.delete()




@app.on_message(gen("ulink", allow = ["sudo", "channel"]))
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




@app.on_message(gen("mlink", allow = ["sudo", "channel"]))
async def get_message_links(_, m: Message):
	reply = m.reply_to_message
	message = reply if reply else m

	m = await app.send_edit(m, "Generating message link . . .", mono=True)
	await app.send_edit(m, message.link)




@app.on_message(gen("saved", allow = ["sudo", "channel"]))
async def save_to_cloud(_, m: Message):
	if m.from_user.is_self:
		await m.delete()
	await m.reply_to_message.copy("me")




@app.on_message(gen(["fwd", "frwd"], allow = ["sudo", "channel"]))
async def forward_msgs(_, m: Message):
	reply = m.reply_to_message
	try:

		if reply and app.long(m) == 1:
			await reply.forward(m.chat.id)

		elif reply and app.long(m) > 1:
			await reply.forward(m.command[1])

		elif not reply and app.long(m) == 1:
			await m.forward(m.text if m.text else "None")

		elif not reply and app.long(m) > 1:
			await app.send_edit(m, "Sir reply to yours or someone's message. to forward.", mono=True, delme=4)

		else:
			await app.send_edit(m, "Something went wrong, please try again later !", mono=True, delme=4)

		if m.from_user.is_self:
			await m.delete()

	except Exception as e:
		await app.error(m, e)




@app.on_message(gen(["spt", "speed", "speedtest"], allow = ["sudo", "channel"]))
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
		m = await app.send_edit(m, "Calculating Speed (pic) . . .")

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
			await app.send_edit(m, "Something went wrong !", mono=True, delme=5)





@app.on_message(gen(["cc", "cchats"], allow = ["sudo", "channel"]))
async def common_chats(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			collect = []
			collect.clear()

			data = await app.get_common_chats(reply.from_user.id)
			for x in data:
				collect.append(x["title"] + "\n")
			if bool(collect):
				await app.send_edit(m, f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "".join(collect))
			else:
				await app.send_edit(m, f"**Common chats with:** `{reply.from_user.first_name}`\n\n" + "`None`")
		else:
			await app.send_edit(m, "Please reply to someone . . .", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)


