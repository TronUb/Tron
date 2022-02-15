import time
import json
import random
import asyncio
import requests

from pyrogram import filters, Client
from pyrogram.errors import FloodWait

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"fun" : (
		"fun",
		{
		"cap [text]" : "Convert a paragraph into capital.",
		"slap [reply to user]" : "Slap your friends with amazing items.",
		"type [text]" : "Retype words with animation, just try and understand, Don't Use too much.",
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
async def slap_friends(app, m):
	if m.reply_to_message:
		try:
			m = await app.send_edit(m,". . .")

			my_info = app.UserMention()
			user = m.reply_to_message.from_user
			user_info = app.mention_markdown(user.id, user.first_name)
			TASK = (
				f"{my_info} slaps {user_info} with a bunch of cardboards",
				f"{my_info} hits {user_info} in the face with cows",
				f"{my_info} ties {user_info} on a chair and rubs him with a sandpaper",
				f"{my_info} helped {user_info} swimming in lava",
				f"{my_info} starts slapping {user_info} with Titanic ship",
				f"{my_info} fills a book of physics in {user_info} mouth",
				f"{my_info} gives a cup of poison to {user_info} ",
				f"{my_info} slaps {user_info} with bunch of dead mosquito",
				f"{my_info} hits {user_info}'s face with rubber chicken",
				f"{my_info} starts puts {user_info} in water with phirana",
				f"{my_info} dumps {user_info} in a river",
				f"{my_info} pats {user_info} on head",
				f"{my_info} kicks {user_info}'s out of the conversation",
			)
			await app.send_edit(m, f"{random.choice(TASK)}")

		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, "Reply to a friend to use harsh words to insult him", delme=2, mono=True)
		return




@app.on_message(gen(["cap", "capital"]))
async def capitalise(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			text = reply.text.capitalize()
			await app.send_edit(m, text)
		elif not reply:
			if app.long(m) > 1:
				text = m.text.split(None, 1)[1].capitalize()
				await app.send_edit(m, text)
			elif app.long(m) == 1:
				await app.send_edit(m, "Please give me some text after command . . .", delme= 2, mono=True)
		else:
			return await app.send_edit(m, "Something went wrong !", mono=True, delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("type"))
async def type_animatiom(_, m):
	try:
		if app.long(m) > 1:
			text = " ".join(m.command[1:])
		else:
			return await app.send_edit(m, "Some text is required to show in typing animation", delme=2)

		tbp = "" 
		typing_symbol = "▒"
		while(tbp != text):
			try:
				await app.send_edit(m, tbp + typing_symbol)
				await asyncio.sleep(0.40)
				tbp = tbp + text[0]
				text = text[1:]
				await app.send_edit(m, tbp)
				await asyncio.sleep(0.40)
			except FloodWait as e:
				time.sleep(e.x) # continue
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("insult"))
async def insult_someone(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can insult them . . .", delme=2, mono=True)
	elif reply:
		try:
			m = await app.send_edit(m, "Insulting . . .", mono=True)
			if app.long(m) == 1:
				lang = "en"
			elif app.long(m) > 1:
				lang = m.command[1]
			data = requests.get(f"https://evilinsult.com/generate_insult.php?lang={lang}&type=json")
			_data = data.json()
			if _data:
				await app.send_edit(m, f"`{_data.get('insult')}`")
			else:
				await app.send_edit(m, "No insults found !", delme=2, mono=True)
		except Exception as e:
			await app.error(m, e)
	else:
		return




@app.on_message(gen("advice"))
async def give_advice(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can give them a advice . . .", delme=2, mono=True)
	elif reply:
		try:
			m = await app.send_edit(m, "Finding a good advice . . .", mono=True)
			data = requests.get(f"https://api.adviceslip.com/advice")
			_data = data.json().get("slip").get("advice")
			if _data:
				await app.send_edit(m, f"`{_data}`")
			else:
				await app.send_edit(m, "No advice found !", delme=2, mono=True)
		except Exception as e:
			await app.error(m, e)
	else:
		return




@app.on_message(gen("qs"))
async def ask_question(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can give them a question . . .", delme=2, mono=True)
	elif reply:
		try:
			m = await app.send_edit(m, "Finding a question . . .", mono=True)
			data = requests.get(f"http://jservice.io/api/random")
			question = data.json()[0].get("question")
			answer = data.json()[0].get("answer")
			if question and answer:
				await app.send_edit(m, f"Question:\n\n`{question}`")
				await app.send_message("me", f"Answer:\n\n`{answer}`") # answer in saved messages
			else:
				await app.send_edit(m, "No question found !", delme=2, mono=True)
		except Exception as e:
			await app.error(m, e)
	else:
		return




@app.on_message(gen("wtd"))
async def what_to_do(_, m):
	try:
		m = await app.send_edit(m, "Finding a activity . . .", mono=True)
		data = requests.get(f"http://www.boredapi.com/api/activity/")
		act = data.json().get("activity")
		typ = data.json().get("type")
		if act:
			await app.send_edit(m, f"Activity: `{act}`\n\nType: `{typ}`") 
		else:
			await app.send_edit(m, "No Activity found !", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("mqt"))
async def movie_quotes(_, m):
	try:
		m = await app.send_edit(m, "Finding a movie quote . . .", mono=True)
		data = requests.get(f"https://movie-quote-api.herokuapp.com/v1/quote/")
		qt = data.json().get("quote")
		role = data.json().get("role")
		show = data.json().get("show")
		if qt and role and show:
			await app.send_edit(m, f"**Quote:**\n\n`{qt}`\n\nRole: `{role}`\n\nShow: `{show}`") 
		else:
			await app.send_edit(m, "No movie quotes found !", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("joke"))
async def send_joke(_, m):
	try:
		m = await app.send_edit(m, "Finding a joke . . .", mono=True)
		data = requests.get(f"https://official-joke-api.appspot.com/random_joke")
		one = data.json().get("setup")
		two = data.json().get("punchline")
		if bool(data) is False:
			return app.send_edit(m, "Site is down, please try again later . . .", delme=2, mono=True)
		if one and two:
			await app.send_edit(m, f"Person: `{one}`\n\nMe: `{two}`") 
		else:
			await app.send_edit(m, "No jokes found !", delme=2, mono=True)
	except Exception as e:
		await app.error(m, e)

