import ( 
	time, 
	random,
	asyncio,
	requests,
	json,
)

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
		"sw [text]" : "Switch words or sentences into japanese alphabets",
		"switch [text]" : "Switch words or Sentence Into Japanese Alphabets.",
		"slap [reply to user]" : "Slap your friends with amazing items.",
		"type [text]" : "Retype words with animation, just try and understand, Don't Use too much.",
		"score [firstname] [secondname]" : "Check love bond between two users.",
		"morse [reply to message]" : "Convert English text messages in morse codes.",
		"demorse [reply to message]" : "Convert morse codes into English text messages."
		}
		)
	}
)




@app.on_message(gen("slap"))
async def insult_friends(app, m):
	if m.reply_to_message:
		try:
			await send_edit(
				m,
				"..."
				)
			my_info = mymention()
			user_ids = m.reply_to_message.from_user.id
			user = await app.get_users(user_ids)
			user_info = mention_markdown(user_ids, user.first_name)
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
			await send_edit(
				m, 
				f"{random.choice(TASK)}"
				)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			"`Reply to a friend to use harsh words to insult him`"
			)
		time.sleep(1)
		await m.delete()
		return




@app.on_message(gen(["cap", "capital"]))
async def switch(_, m):
	ja_keys = """`abcdefghijklmnopqrstuvwxyz1234567890`"""
	en_keys = """`ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`"""
	try:
		if m.reply_to_message:
			reply_text = m.reply_to_message.text
			change = str.maketrans(ja_keys + en_keys, en_keys + ja_keys)
			reply_text = str.translate(reply_text, change)
			await send_edit(
				m, 
				reply_text
				)
		elif len(m.text) > 1:
			text = m.text.split(None, 1)[1]
			change = str.maketrans(ja_keys + en_keys, en_keys + ja_keys)
			text = str.translate(text, change)
			await send_edit(
				m, 
				text
				)
			await asyncio.sleep(1)
		else:
			await send_edit(
				m, 
				f"Reply to a message or type `{PREFIX}sw [this is a text]`"
				)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("type"))
async def type(_, m):
	try:
		if len(m.text) > 1:
			text = " ".join(m.command[1:])
		else:
			await send_edit(
				m, 
				"Some text is required to show in typing animation"
				)
			asyncio.sleep(2)
			await m.delete()
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
		await send_edit(m, "Please reply to someone, so that i can insult them . . .")
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
				await send_edit(m, f"`{_data.get("insult")}`")
			else:
				send_edit(m, "No insults found !")
		except Exception as e:
			await error(m, e)
	else:
		return
