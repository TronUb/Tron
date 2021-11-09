import requests, json

from tronx import (
	app, 
	CMD_HELP,
)

from tronx.helpers import (
	gen,
	error,
)





anime_suffix = "`baka`\n`bite`\n`blush`\n`bored`\n`cry`\n`cuddle`\n`dance`\n`facepalm`\n`feed`\n`happy`\n`highfive`\n`hug`\n`kiss`\n`laugh`\n`pat`\n`poke`\n`pout`\n`shrug`\n`slap`\n`sleep`\n`smile`\n`stare`\n`think`\n`thumbsup`\n`tickle`\n`wave`\n`wink`"




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




@app.on_message(gen("gif"))
async def baka_gif(_, m):
	if long(m) > 1:
		arg = m.command[1]
		try:
			await m.delete()
			if arg == "baka":
				data = get_anime_gif("baka")
				await send_gif(m, data)
			elif arg == "bite":
				data = get_anime_gif("bite")
				await send_gif(m, data)
			elif arg == "blush":
				data = get_anime_gif("blush")
				await send_gif(m, data)
			elif arg == "bored":
				data = get_anime_gif("bored")
				await send_gif(m, data)
			elif arg == "cry":
				data = get_anime_gif("cry")
				await send_gif(m, data)
			elif arg == "cuddle":
				data = get_anime_gif("cuddle")
				await send_gif(m, data)
			elif arg == "dance":
				data = get_anime_gif("dance")
				await send_gif(m, data)
			elif arg == "facepalm":
				data = get_anime_gif("facepalm")
				await send_gif(m, data)
			elif arg ==  "feed":
				data = get_anime_gif("feed")
				await send_gif(m, data)
			elif arg == "happy":
				data = get_anime_gif("happy")
				await send_gif(m, data)
			elif arg == "highfive":
				data = get_anime_gif("highfive")
				await send_gif(m, data)
			elif arg == "hug":
				data = get_anime_gif("hug")
				await send_gif(m, data)
			elif arg == "kiss":
				data = get_anime_gif("kiss")
				await send_gif(m, data)
			elif arg == "laugh":
				data = get_anime_gif("laugh")
				await send_gif(m, data)
			elif arg == "pat":
				data = get_anime_gif("pat")
				await send_gif(m, data)
			elif arg == "poke":
				data = get_anime_gif("poke")
				await send_gif(m, data)
			elif arg == "pout":
				data = get_anime_gif("pout")
				await send_gif(m, data)
			elif arg == "shrug":
				data = get_anime_gif("shrug")
				await send_gif(m, data)
			elif arg == "sleep":
				data = get_anime_gif("sleep")
				await send_gif(m, data)
			elif arg == "slap":
				data = get_anime_gif("slap")
				await send_gif(m, data)
			elif arg == "smile":
				data = get_anime_gif("smile")
				await send_gif(m, data)
			elif arg == "smug":
				data = get_anime_gif("smug")
				await send_gif(m, data)
			elif arg == "stare":
				data = get_anime_gif("stare")
				await send_gif(m, data)
			elif arg == "think":
				data = get_anime_gif("think")
				await send_gif(m, data)
			elif arg == "thumbsup":
				data = get_anime_gif("thumbsup")
				await send_gif(m, data)
			elif arg == "tickle":
				data = get_anime_gif("tickle")
				await send_gif(m, data)
			elif arg == "wave":
				data = get_anime_gif("wave")
				await send_gif(m, data)
			elif arg == "wink":
				data = get_anime_gif("wink")
				await send_gif(m, data)
			elif arg == "think":
				data = get_anime_gif("think")
				await send_gif(m, data)
			else:
				await send_edit(m, anime_suffix)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(m, "Give me a suffix . . .", mono=True, delme=3)
