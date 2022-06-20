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
		"upcase [text]" : "Convert texts into uppercase",
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




@app.on_message(gen("slap", allow =["sudo"]))
async def slap_handler(_, m):
	if m.reply_to_message:
		try:
			m = await app.send_edit(m,". . .")

			my_info = app.UserMention()
			user = m.reply_to_message.from_user
			user_info = user.mention
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
				f"{my_info} kicks {user_info} out of the conversation",
			)
			await app.send_edit(m, f"{random.choice(TASK)}")

		except Exception as e:
			await app.error(m, e)
	else:
		await app.send_edit(m, "Reply to a friend to use harsh words to insult him", delme=2, text_type=["mono"])




@app.on_message(gen(["upcase"], allow =["sudo"]))
async def uppercase_handler(_, m):
	try:
		reply = m.reply_to_message
		if reply:
			text = reply.text.upper()
			await app.send_edit(m, text)
		elif not reply:
			if app.long(m) > 1:
				text = m.text.split(None, 1)[1].upper()
				await app.send_edit(m, text)
			elif app.long(m) == 1:
				await app.send_edit(m, "Please give me some text after command . . .", delme= 2, text_type=["mono"])
		else:
			return await app.send_edit(m, "Something went wrong !", text_type=["mono"], delme=4)
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("type", allow =["sudo"]))
async def type_handler(_, m):
	try:
		if app.long(m) > 1:
			text = [x for x in m.text.split(None, 1)[1]]
		else:
			return await app.send_edit(m, "Some text is required to show in typing animation", delme=2)

		tbp = "" 
		typing_symbol = "▒"
		for i in range(len(text)):
			try:
				await app.send_edit(m, tbp + typing_symbol)
				await asyncio.sleep(0.40)
				tbp = tbp + text[i]
				await app.send_edit(m, tbp)
				await asyncio.sleep(0.40)
			except FloodWait as e:
				time.sleep(e.x) # continue
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("insult", allow =["sudo"]))
async def insult_handler(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can insult them . . .", delme=2, text_type=["mono"])
	elif reply:
		try:
			if app.long(m) == 1:
				lang = "en"
			elif app.long(m) > 1:
				lang = m.command[1]
			data = requests.get(f"https://evilinsult.com/generate_insult.php?lang={lang}&type=json")
			_data = data.json()

			m = await app.send_edit(m, "Insulting . . .", text_type=["mono"])
			if _data:
				await app.send_edit(m, f"`{_data.get('insult')}`")
			else:
				await app.send_edit(m, "No insults found !", delme=4, text_type=["mono"])
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen("advice", allow =["sudo"]))
async def advice_handler(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can give them a advice . . .", delme=2, text_type=["mono"])
	elif reply:
		try:
			m = await app.send_edit(m, "Finding a good advice . . .", text_type=["mono"])
			data = requests.get(f"https://api.adviceslip.com/advice")
			_data = data.json().get("slip").get("advice")
			if _data:
				await app.send_edit(m, f"`{_data}`")
			else:
				await app.send_edit(m, "No advice found !", delme=2, text_type=["mono"])
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen("qs", allow =["sudo"]))
async def question_handler(_, m):
	reply = m.reply_to_message
	if not reply:
		await app.send_edit(m, "Please reply to someone, so that i can give them a question . . .", delme=2, text_type=["mono"])
	elif reply:
		try:
			m = await app.send_edit(m, "Finding a question . . .", text_type=["mono"])
			data = requests.get(f"http://jservice.io/api/random")
			question = data.json()[0].get("question")
			answer = data.json()[0].get("answer")
			if question and answer:
				await app.send_edit(m, f"Question:\n\n`{question}`")
				await app.send_message("me", f"Answer:\n\n`{answer}`") # answer in saved messages
			else:
				await app.send_edit(m, "No question found !", delme=2, text_type=["mono"])
		except Exception as e:
			await app.error(m, e)




@app.on_message(gen("wtd", allow =["sudo"]))
async def whattodo_handler(_, m):
	try:
		m = await app.send_edit(m, "Finding a activity . . .", text_type=["mono"])
		data = requests.get(f"http://www.boredapi.com/api/activity/")
		act = data.json().get("activity")
		typ = data.json().get("type")
		if act:
			await app.send_edit(m, f"Activity: `{act}`\n\nType: `{typ}`") 
		else:
			await app.send_edit(m, "No Activity found !", delme=2, text_type=["mono"])
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("mqt", allow =["sudo"]))
async def moviequote_handler(_, m):
	try:
		m = await app.send_edit(m, "Finding a movie quote . . .", text_type=["mono"])
		data = requests.get(f"https://movie-quote-api.herokuapp.com/v1/quote/")
		qt = data.json().get("quote")
		role = data.json().get("role")
		show = data.json().get("show")
		if qt and role and show:
			await app.send_edit(m, f"**Quote:**\n\n`{qt}`\n\nRole: `{role}`\n\nShow: `{show}`") 
		else:
			await app.send_edit(m, "No movie quotes found !", delme=2, text_type=["mono"])
	except Exception as e:
		await app.error(m, e)




@app.on_message(gen("joke", allow =["sudo"]))
async def joke_handler(_, m):
	try:
		m = await app.send_edit(m, "Finding a joke . . .", text_type=["mono"])
		data = (requests.get("https://icanhazdadjoke.com/slack").json())["attachments"][0]["fallback"]
		if bool(data) is False:
			return app.send_edit(m, "Site is down, please try again later . . .", delme=3, text_type=["mono"])
		elif data:
			await app.send_edit(m, f"{data}") 
		else:
			await app.send_edit(m, "No jokes found !", delme=2, text_type=["mono"])
	except Exception as e:
		await app.send_edit(m, "Server error, try again later.", text_type=["mono"], delme=4)
		await app.error(m, e)

