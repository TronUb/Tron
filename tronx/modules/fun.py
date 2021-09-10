import time, random,asyncio,requests, json

from pyrogram import filters, Client
from pyrogram.errors import FloodWait

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX,
	USER_NAME,
	USER_ID
	)

from tronx.helpers import (
	error,
	mymention,
	gen,
	send_edit,
	# others 
	mention_markdown,
	long,
)




CMD_HELP.update(
	{"fun" : (
		"fun",
		{
		"cap [text]" : "Convert a paragraph into capital.",
		"slap [reply to user]" : "Slap your friends with amazing items.",
		"type [text]" : "Retype words with animation, just try and understand, Don't Use too much.",
		"score [firstname] [secondname]" : "Check love bond between two users.",
		"morse [reply to message]" : "Convert English text messages in morse codes.",
		"demorse [reply to message]" : "Convert morse codes into English text messages.",
		"insult [reply to message]" : "Use it to insult idiots & fools",
		"advice [reply to message]" : "get a random advice for someone.",
		"wtd" : "what to do when you are bored ?, finds a activity for you.",
		"mqt" : "Finds some movie quotes for you.",
		"joke" : "Get some daddy jokes.",
		}
		)
	}
)




@app.on_message(gen("slap"))
async def insult_friends(app, m):
	if m.reply_to_message:
		try:
			await send_edit(m,"...")

			my_info = mymention()
			user = m.reply_to_message.from_user
			user_info = mention_markdown(user.id, user.first_name)
			TASK = (
				f"{my_info} slaps {user_info} with a bunch of cardboards",
				f"{my_info} hits {user_info} in the face with cows",
				f"{my_info} ties {user_info} on a chair and rubs him with a sandpaper",
				f"{my_info} helped {user_info} swimming in lava",
				f"{my_info} starts slapping {user_info} with Titanic ship",
				f"{my_info} fills a book of physics in {user_info} mouth",
				f"{my_info} gives a cup of poison to {user_info} ",
				f"{my_info} slaps {user_info} with bunch of dead mosquito",
				f"{my_info} hits {user_info} face with rubber chicken",
				f"{my_info} starts puts {user_info} in water with phirana",
				f"{my_info} dumps {user_info} in a river",
				f"{my_info} pats {user_info} on head",
				f"{my_info} kicks {user_info}'s out of the conversation",
			)
			await send_edit(m, f"{random.choice(TASK)}")

		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "`Reply to a friend to use harsh words to insult him`", delme=2)
		return




@app.on_message(gen(["cap", "capital"]))
async def switch(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			text = reply.text.capitalize()
			await send_edit(m, text)
		elif not reply:
			if long(m) > 1:
				text = m.text.split(None, 1)[1]
				await send_edit(m, text)
			elif long(m) == 1:
				await send_edit(m, "Please give me some text after command . . .", delme= 2)
		else:
			return print("error in cap command")
	except Exception as e:
		await error(m, e)




@app.on_message(gen("type"))
async def type(_, m):
	try:
		if len(m.text) > 1:
			text = " ".join(m.command[1:])
		else:
			await send_edit(m, "Some text is required to show in typing animation", delme=2)
			return
		tbp = "" 
		typing_symbol = "▒"
		while(tbp != text):
			try:
				await send_edit(m, 
				tbp + typing_symbol
				)
				await asyncio.sleep(0.40)
				tbp = tbp + text[0]
				text = text[1:]
				await send_edit(
					m, 
					tbp
					)
				await asyncio.sleep(0.40)
			except FloodWait as e:
				time.sleep(e.x) # continue
	except IndexError:
		pass




@app.on_message(gen("insult"))
async def insult_someone(_, m):
	reply = m.reply_to_message
	if not reply:
		await send_edit(m, "Please reply to someone, so that i can insult them . . .", delme=2)
	elif reply:
		try:
			await send_edit(m, "Insulting . . .")
			if long(m) == 1:
				lang = "en"
			elif long(m) > 1:
				lang = m.command[1]
			data = requests.get(f"https://evilinsult.com/generate_insult.php?lang={lang}&type=json")
			_data = data.json()
			if _data:
				await send_edit(m, f"`{_data.get('insult')}`")
			else:
				await send_edit(m, "No insults found !", delme=2)
		except Exception as e:
			await error(m, e)
	else:
		return




@app.on_message(gen("advice"))
async def give_advice(_, m):
	reply = m.reply_to_message
	if not reply:
		await send_edit(m, "Please reply to someone, so that i can give them a advice . . .", delme=2)
	elif reply:
		try:
			await send_edit(m, "Finding a good advice . . .")
			data = requests.get(f"https://api.adviceslip.com/advice")
			_data = data.json().get("slip").get("advice")
			if _data:
				await send_edit(m, f"`{_data}`")
			else:
				await send_edit(m, "No advice found !", delme=2)
		except Exception as e:
			await error(m, e)
	else:
		return




@app.on_message(gen("qs"))
async def insult_someone(_, m):
	reply = m.reply_to_message
	if not reply:
		await send_edit(m, "Please reply to someone, so that i can give them a question . . .", delme=2)
	elif reply:
		try:
			await send_edit(m, "Finding a question . . .")
			data = requests.get(f"http://jservice.io/api/random")
			question = data.json()[0].get("question")
			answer = data.json()[0].get("answer")
			if question and answer:
				await send_edit(m, f"Question:\n\n`{question}`")
				await app.send_message("me", f"Answer:\n\n`{answer}`") # answer in saved messages
			else:
				await send_edit(m, "No question found !", delme=2)
		except Exception as e:
			await error(m, e)
	else:
		return




@app.on_message(gen("wtd"))
async def what_to_do(_, m):
	try:
		await send_edit(m, "Finding a activity . . .")
		data = requests.get(f"http://www.boredapi.com/api/activity/")
		act = data.json().get("activity")
		typ = data.json().get("type")
		if act:
			await send_edit(m, f"Activity: `{act}`\n\nType: `{typ}`") 
		else:
			await send_edit(m, "No Activity found !", delme=2)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("mqt"))
async def movie_quotes(_, m):
	try:
		await send_edit(m, "Finding a movie quote . . .")
		data = requests.get(f"https://movie-quote-api.herokuapp.com/v1/quote/")
		qt = data.json().get("quote")
		role = data.json().get("role")
		show = data.json().get("show")
		if qt and role and show:
			await send_edit(m, f"Quote: `{qt}`\n\nRole: `{role}`\n\nShow: `{show}`") 
		else:
			await send_edit(m, "No movie quotes found !", delme=2)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("joke"))
async def tell_me_a_joke(_, m):
	try:
		await send_edit(m, "Finding a joke . . .")
		data = requests.get(f"https://movie-quote-api.herokuapp.com/v1/quote/")
		one = data.json().get("setup")
		two = data.json().get("punchline")
		if one and two:
			await send_edit(m, f"Person: `{one}`\n\nMe: `{two}`") 
		else:
			await send_edit(m, "No jokes found !", delme=2)
	except Exception as e:
		await error(m, e)

