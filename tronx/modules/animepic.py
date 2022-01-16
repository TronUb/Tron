import requests, json

from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	PREFIX,
)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	long,
)





anime_suffix = "`baka`\n`bite`\n`blush`\n`bored`\n`cry`\n`cuddle`\n`dance`\n`facepalm`\n`feed`\n`happy`\n`highfive`\n`hug`\n`kiss`\n`laugh`\n`pat`\n`poke`\n`pout`\n`shrug`\n`slap`\n`sleep`\n`smile`\n`stare`\n`think`\n`thumbsup`\n`tickle`\n`wave`\n`wink`"
anime_list = ["baka", "bite", "blush", "bored", "cry", "cuddle", "dance", "facepalm", "feed", "happy", "highfive", "hug", "kiss", "laugh", "pat", "poke", "pout", "shrug", "slap", "sleep", "smile", "stare", "think", "thumbsup", "tickle", "wave", "wink"]




CMD_HELP.update(
	{"animepic": (
		"animepic",
		{
		"neko" : "Get a anime neko girl image.",
		"gif [suffix]" : "Get gif's of different anime expressions, use the command below to get suffix list.",
		"giflist" : "Get a list of suffix.",
		}
		)
	}
)





def get_anime_gif(arg):
	data = requests.get(f"https://nekos.best/api/v1/{arg}").text
	img = json.loads(data)["url"]
	text = json.loads(data)["anime_name"]
	if img and text:
		return [img, text]
	else:
		return False



async def send_gif(m: Message, gif_data):
	try:
		await app.send_video(
			m.chat.id,
			gif_data[0],
			caption=gif_data[1]
		)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("giflist"))
async def list_of_suffix(_, m):
	await send_edit(m, anime_suffix)



	
@app.on_message(gen("neko"))
async def baka_gif(_, m):
	try:
		await m.delete()
		data = requests.get("https://nekos.best/api/v1/nekos").text
		data = json.loads(data)
		await app.send_photo(
			m.chat.id,
			data["url"],
			caption = data["artist_name"]
			)
	except Exception as e:
		await error(m, e)




@app.on_message(gen("animegif"))
async def baka_gif(_, m):
	if long(m) > 1:
		arg = m.command[1]
		try:
			await m.delete()
			if arg in anime_list:
				data = get_anime_gif(arg)
				await send_gif(m, data)
			else:
				await send_edit(m, anime_suffix)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, f"Give me a suffix, use `{PREFIX}giflist` to get suffix . . .", delme=5)
