import requests

from pyrogram.types import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	CallbackQuery,
	Message,
)

from pyrogram import filters

from tronx import bot

from tronx.helpers.bot_helper import (
	airing_query,
	anime_query,
	character_query,
	manga_query,
	shorten,
	sec,
)

from tronx.helpers import error




url = "https://graphql.anilist.co"


@bot.on_message(filters.command("airing"))
async def anime_airing(_, m):
	try:
		await infoairing(m)
	except Exception as e:
		await error(m, e)




async def infoairing(m: Message):
	search_str = m.text.split(" ", 1)
	if len(search_str) == 1:
		await m.reply("Example: `/airing demon slayer`")
		return

	variables = {"search": search_str[1]}
	response = requests.post(
		url, json={"query": airing_query, "variables": variables}
	).json()["data"]["Media"]
	ms_g = f"<b>Name</b>: <b>{response['title']['romaji']}</b>(<code>{response['title']['native']}</code>)\n<b>ID</b>: <code>{response['id']}</code>"
	if response["nextAiringEpisode"]:
		airing_time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
		airing_time_final = t(airing_time)
		ms_g += f"\n<b>Episode</b>: <code>{response['nextAiringEpisode']['episode']}</code>\n<b>Airing In</b>: <code>{airing_time_final}</code>"
	else:
		ms_g += f"\n<b>Episode</b>: <code>{response['episodes']}</code>\n<b>Status</b>: <code>N/A</code>"
	await m.reply(ms_g)
	return




@bot.on_message(filters.command("anime"))
async def anime_search(_, m):
	try:
		await infoanime(m)
	except Exception as e:
		await error(m, e)




async def infoanime(m: Message):
	search = m.text.split(" ", 1)
	if len(search) == 1:
		await m.reply("Example: `/anime demon slayer`")
		return
	else:
		search = search[1]
	variables = {"search": search}
	json = (
		requests.post(url, json={"query": anime_query, "variables": variables})
		.json()["data"]
		.get("Media", None)
	)
	if json:
		msg = f"<b>{json['title']['romaji']}</b>(<code>{json['title']['native']}</code>)\n<b>Type</b>: {json['format']}\n<b>Status</b>: {json['status']}\n<b>Episodes</b>: {json.get('episodes', 'N/A')}\n<b>Duration</b>: {json.get('duration', 'N/A')} Per Ep.\n<b>Score</b>: {json['averageScore']}\n<b>Genres</b>: <code>"
		for x in json["genres"]:
			msg += f"{x}, "
		msg = msg[:-2] + "</code>\n"
		msg += "<b>Studios</b>: <code>"
		for x in json["studios"]["nodes"]:
			msg += f"{x['name']}, "
		msg = msg[:-2] + "</code>\n"
		info = json.get("siteUrl")
		trailer = json.get("trailer", None)
		if trailer:
			trailer_id = trailer.get("id", None)
			site = trailer.get("site", None)
			if site == "youtube":
				trailer = "https://youtu.be/" + trailer_id
		description = (
			json.get("description", "N/A")
			.replace("<i>", "")
			.replace("</i>", "")
			.replace("<br>", "")
		)
		msg += shorten(description, info)
		image = info.replace("anilist.co/anime/", "img.anili.st/media/")
		if trailer:
			buttons = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"More Info",
							url = "info",
						)
					],
					[
						InlineKeyboardButton(
							"Trailer",
							url = trailer,
						)
					],
				]
				)
		else:
			buttons = InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton(
							"More Info",
							url = info
						)
					],
				]
				)
		if image:
			try:
				await m.reply_photo(image, caption=msg, reply_markup=buttons)
			except:
				msg += f" [🌐]({image})"
				await m.reply(msg)
		else:
			await m.reply(msg)
	return




@bot.on_message(filters.command("character"))
async def character_search(_, m):
	try:
		await infocharacter(m)
	except Exception as e:
		await error(m, e)




async def infocharacter(m: Message):
	search = m.text.split(" ", 1)
	if len(search) == 1:
		await m.reply("Example: `/character shino asada`")
		return
	search = search[1]
	variables = {"query": search}
	json = (
		requests.post(url, json={"query": character_query, "variables": variables})
		.json()["data"]
		.get("Character", None)
	)
	if json:
		ms_g = f"<b>{json.get('name').get('full')}</b>(<code>{json.get('name').get('native')}</code>)\n"
		description = (f"{json['description']}").replace("__", "")
		site_url = json.get("siteUrl")
		ms_g += shorten(description, site_url)
		image = json.get("image", None)
		if image:
			image = image.get("large")
			await m.reply_photo(image, caption=ms_g)
		else:
			await m.reply(ms_g)
	else:
		await m.reply("Character not found !")
	return




@bot.on_message(filters.command("manga"))
async def manga_search(_, m):
	try:
		await infomanga(m)
	except Exception as e:
		await error(m, e)




async def infomanga(m: Message):
	search = m.text.split(" ", 1)
	if len(search) == 1:
		await m.reply("Example: /manga demon slayer")
		return
	search = search[1]
	variables = {"search": search}
	json = (
		requests.post(url, json={"query": manga_query, "variables": variables})
		.json()["data"]
		.get("Media", None)
	)
	ms_g = ""
	if json:
		title, title_native = json["title"].get("romaji", False), json["title"].get(
			"native", False
		)
		start_date, status, score = (
			json["startDate"].get("year", False),
			json.get("status", False),
			json.get("averageScore", False),
		)
		if title:
			ms_g += f"<b>{title}</b>"
			if title_native:
				ms_g += f"(<code>{title_native}</code>)"
		if start_date:
			ms_g += f"\n<b>Start Date</b> - <code>{start_date}</code>"
		if status:
			ms_g += f"\n<b>Status</b> - <code>{status}</code>"
		if score:
			ms_g += f"\n<b>Score</b> - <code>{score}</code>"
		ms_g += "\n<b>Genres</b> - "
		for x in json.get("genres", []):
			ms_g += f"{x}, "
		ms_g = ms_g[:-2]

		image = json.get("bannerImage", False)
		ms_g += (
			(f"\n<i>{json.get('description', None)}</i>")
			.replace("<br>", "")
			.replace("</br>", "")
		)
		if image:
			try:
				await m.reply_photo(image, caption=ms_g)
			except:
				ms_g += f" [〽️]({image})"
				await m.reply(ms_g)
		else:
			await m.reply(ms_g)
	else:
		await m.reply("Not Found !")
	return




def quote():
	results = requests.get("https://animechan.vercel.app/api/random").json()
	msg = f"❝ {results.get('quote')} ❞"
	msg += f" [ {results.get('anime')} ]\n\n"
	msg += f"- {results.get('character')}\n\n"
	return msg




@bot.on_message(filters.command(["quote"]) & filters.incoming)
async def anime_quotes(client, m):
	await bot.send_message(
		m.chat.id,
		quote(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"More", callback_data="more-anime-quotes",
					),
				]
			]
		),
	)




@bot.on_callback_query(filters.regex("more-anime-quotes"))
async def modules(c, cb):
	await cb.edit_message_text(
		quote(),
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(
						"More", callback_data="more-anime-quotes",
					),
				]
			]
		),
	)



