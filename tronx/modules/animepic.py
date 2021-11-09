import requests, json

from tronx import (
	app
)

from tronx.helpers import (
	gen,
	error,
)




CMD_HELP.update(
	{"animepic": (
		"animepic",
		{
		"neko" : "Get a anime neko girl image",
		}
		)
	}
)




def get_anime_gif(arg):
	data = requests.get(f"https://nekos.best/api/v1/{arg}").text
	img = json.loads(data)["url"], 
	text = json.loads(data)["anime_name"]
	if img and text:
		return ([img, text])
	else:
		return False




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




@app.on_message(gen("bakagif"))
async def baka_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("baka")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("bitegif"))
async def bite_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("bite")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("blushgif"))
async def blush_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("blush")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("boredgif"))
async def bored_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("bored")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("crygif"))
async def cry_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("cry")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("cuddlegif"))
async def cuddle_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("cuddle")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("dancegif"))
async def dance_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("dance")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("facepalmgif"))
async def facepalm_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("facepalm")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("feedgif"))
async def feed_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("feed")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("happygif"))
async def happy_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("happy")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("highfivegif"))
async def highfive_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("highfive")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("huggif"))
async def hug_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("hug")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("kissgif"))
async def kiss_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("kiss")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("laughgif"))
async def laugh_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("laugh")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("patgif"))
async def pat_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("pat")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("pokegif"))
async def poke_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("poke")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("poutgif"))
async def pout_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("pout")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("shruggif"))
async def shrug_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("shrug")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("sleepgif"))
async def sleep_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("sleep")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("slapgif"))
async def slap_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("slap")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("smilegif"))
async def smile_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("smile")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("smuggif"))
async def smug_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("smug")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("staregif"))
async def stare_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("stare")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("thinkgif"))
async def think_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("think")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("thumbsupgif"))
async def thumbsup_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("thumbsup")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("ticklegif"))
async def ticle_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("tickle")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("wavegif"))
async def wave_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("wave")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)





@app.on_message(gen("winkgif"))
async def wink_gif(_, m):
	try:
		await m.delete()
		data = get_anime_gif("wink")
		await app.send_video(
			m.chat.id,
			data[0],
			caption=data[1]
			)
	except Exception as e:
		await error(m, e)
