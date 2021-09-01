import os
import sys
import time
import math
import requests
import heroku3
import asyncio
import json

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP, 
	USER_NAME,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	mymention,
)




CMD_HELP.update(
	{"heroku" : (
		"heroku",
		{
		"shutdown" : "Turn off your userbot by turning off the dynos.",
		"restart" : "Restart your userbot.",
		"usage" : "Check your heroku dyno usage.",
		"vars" : "Get a list of enabled vars in your heroku account.",
		"setvar [key] [value]" : "Set config vars of heroku through a command.",
		"logs" : "Get heroku logs as a file (Extension: .txt).",
		"textlogs" : "Get logs pasted in nekobin, not as a file."
		}
		)
	}
)




heroku_api = "https://api.heroku.com"

useragent = (
	"Mozilla/5.0 (Linux; Android 9; SM-G975F) "
	"AppleWebKit/537.36 (KHTML, like Gecko) "
	"Chrome/80.0.3987.149 Mobile Safari/537.36"
)




# shut-down dyno 
@app.on_message(gen("shutdown"))
async def turn_off_dyno(app, m):
	if Config.LOG_CHAT:
		await app.send_message(
			Config.LOG_CHAT, 
			"#shutdown \n" 
			"Bot is turned off !!"
			)
	if not Config.HEROKU_APP_NAME and Config.HEROKU_API_KEY:
		await m.edit(
			"Please fill HEROKU_APP_NAME and HEROKU_API_KEY Values."
			)
		return
	else:
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY).apps()[Config.HEROKU_APP_NAME]
		if Heroku:
			Heroku.process_formation()["worker"].scale(0)
			await m.edit(
				"`Dynos are truned off, Now turn them manually if you want !!`"
			)
		else:
			sys.exit(0)




# restart your bot 
@app.on_message(gen("restart"))
async def restart(app, m: Message):
	if not (Config.HEROKU_API_KEY and Config.HEROKU_APP_NAME):
		await m.edit_text(
			"Please add `HEROKU_APP_NAME` or `HEROKU_API_KEY` in your Config Vars or file."
		)
		return
	try:
		await m.edit("`Restarting...`")
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		heroku_app = Heroku.apps()[Config.HEROKU_APP_NAME]
		check = heroku_app.restart()
		if check:
			await m.edit(
				"`Restarted...!`\nPlease wait for 5 min to reboot userbot..."
			)
			return
		else:
			await m.edit(
				"`Failed to restart userbot, try again later..."
			)
			return
	except Exception as e:
		await error(m, e)




# get usage of your dyno hours from heroku
@app.on_message(gen("usage"))
async def dynostats(app, m: Message):
	Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
	msg = await m.edit("...")
	u_id = Heroku.account().id
	try:
		if Config.HEROKU_API_KEY is not None:
			headers = {
				"User-Agent": useragent,
				"Authorization": f"Bearer {Config.HEROKU_API_KEY}",
				"Accept": "application/vnd.heroku+json; version=3.account-quotas",
			}
			path = "/accounts/" + u_id + "/actions/get-quota"
			r = requests.get(heroku_api + path, headers=headers)
			if r.status_code != 200:
				await msg.edit(
					"`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
				)
			result = r.json()
			quota = result["account_quota"]
			quota_used = result["quota_used"]
			# used hours
			remaining_quota = quota - quota_used
			percentage = math.floor(remaining_quota / quota * 100)
			minutes_remaining = remaining_quota / 60
			hours = math.floor(minutes_remaining / 60)
			minutes = math.floor(minutes_remaining % 60)
			# remaining
			App = result["apps"]
			try:
				App[0]["quota_used"]
			except IndexError:
				AppQuotaUsed = 0
				AppPercentage = 0
			else:
				AppQuotaUsed = App[0]["quota_used"] / 60
				AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
			AppHours = math.floor(AppQuotaUsed / 60)
			AppMinutes = math.floor(AppQuotaUsed % 60)
			await asyncio.sleep(2)
			await msg.edit(
				"**Dyno Usage**:\n\n"
				f"**Total Dyno Hours:** 550 Hours\n\n"
				f"**⧓ Dyno usage for App:** __`{Config.HEROKU_APP_NAME}`__\n"
				f"\r• `{AppHours}h {AppMinutes}m`"
				f"**|**  [ `{AppPercentage}`**%** ]\n\n"
				f"**⧓ Quota remaining this month:**\n"
				f"\r• `{hours} Hours & {minutes} Mins`"
				f" |  [ `{percentage}%` ]"
			)
	except Exception as e:
		await error(m, e)




# get list of vars from heroku 
@app.on_message(gen("vars"))
async def heroku_vars(app, m: Message):
	if (Config.HEROKU_API_KEY or Config.HEROKU_APP_NAME) is None:
		await m.edit_text(
			"Please add `HEROKU_APP_NAME` and `HEROKU_API_KEY` in your Heroku Config Vars."
		)
		return
	try:
		await m.edit_text("**__Fetching all vars from Heroku...__**")
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		heroku_app = Heroku.apps()[Config.HEROKU_APP_NAME]
		config = heroku_app.config()
		vars_dict = config.to_dict()
		vars_keys = list(vars_dict.keys())
		msg = "**Here are vars setup for Tronuserbot**\n\n"
		num = 0
		for i in vars_keys:
			num += 1
			msg += f"**{num}**: `{i}`\n"

		msg += f"\n**Total <u>{num}</u> Vars are setup!**"
		await m.edit_text(
			msg
		)
		return
	except Exception as e:
		await error(m, e)




# set vars in heroku 
@app.on_message(gen("setvar"))
async def setvar(app, m: Message):
	Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
	zen = Heroku.app(Config.HEROKU_APP_NAME)
	if not Config.HEROKU_APP_NAME:
		await m.edit(
			"Please fill Values of •> HEROKU_APP_NAME"
		)
		return
	elif (len(m.command)) < 3 or (len(m.command)) > 3:
		await m.edit(
			f"`{PREFIX}setvar «key» «value»`"
		)
		return
	elif len(m.command) == 3:
		key = m.command[1]
		value = m.command[2]
		heroku_vars = zen.config()
		try:
			if key and value in heroku_vars:
				await message.edit(
					f"{key} is already in vars with value {value}"
				)
			elif not key in heroku_vars:
				await m.edit(
					f"Added var •> [ {key} = {value} ]", disable_web_page_preview=True
				)
				heroku_vars[key] = value
				time.sleep(1)
				if Config.LOG_CHAT:
					await app.send_message(
						Config.LOG_CHAT, 
						f"#HEROKU_VAR #SET #ADDED\n\n{key} = {value}"
					)
				else:
					await m.edit(
						"Something wrong with `LOG_CHAT`"
					)
			else:
				await m.edit(
					"Something went wrong !"
				)
		except Exception as e:
			await error(m, e)




# get vars from heroku vars
@app.on_message(gen("getvar"))
async def getvar(app, m: Message):
	if not Config.HEROKU_APP_NAME:
		await m.edit(
			"Please fill Values of •> HEROKU_APP_NAME"
		)
		return
	elif (len(m.command)) < 2 or (len(m.command)) > 2:
		await m.edit(
			f"`{PREFIX}setvar «key» «value»`"
		)
		return
	elif len(m.command) == 2:
		key = m.command[1]
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		heroku_app = Heroku.apps()[Config.HEROKU_APP_NAME]
		config = heroku_app.config()
		try:
			if config:
				await m.edit(
					f"{key} = `{config[key]}`"
				)
				time.sleep(1)
				if Config.LOG_CHAT:
					await app.send_message(
						Config.LOG_CHAT, 
						f"#HEROKU_VAR #GET\n\n{key}"
						)
				else:
					await m.edit(
						"Please set `LOG_CHAT`"
						)
			else:
				await m.edit(
					"Failed to get heroku keys..."
					)
		except Exception as e:
			await error(m, e)




# delete vars in heroku 
@app.on_message(gen("delvar"))
async def delvar(app, m: Message):
	if not Config.HEROKU_APP_NAME:
		await m.edit(
			"Please fill Values of •> HEROKU_APP_NAME"
		)
		return
	elif (len(m.command)) < 2 or (len(m.command)) > 2:
		await m.edit(
			f"`{PREFIX}setvar «key» «value»`"
		)
		return
	elif len(m.command) == 2:
		await m.edit(
			"`Verifying var in heroku config vars...`"
		)
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		heroku_app = Heroku.apps()[Config.HEROKU_APP_NAME]
		config = heroku_app.config()
		try:
			key = m.command[1]
		except IndexError:
			await m.edit(
				"Usage: `.delvar USER_PIC` use this format ..."
			)
		time.sleep(1.5)
		return
		if key not in config:
			await m.edit(
				f"**`{key}`** does not exist in heroku vars ..."
			)
			return
		try:
			del config[key]
		except Exception as e:
			await error(app, m, e)
		await m.edit(
			f"**`{key}`** Deleted Successfully from heroku vars ... !!"
		)
	else:
		await m.edit(
			"Usage: `.delvar USER_PIC` use this format ..."
		)
		time.sleep(1.5)




# get logs from heroku in file format (.txt)
@app.on_message(gen("logs"))
async def logs(app, m: Message):
	user = await app.get_me()
	user = user.username
	await m.edit(
		"⏳ • hold on...")
		
	if not Config.HEROKU_APP_NAME:
		await m.edit(
			"Please fill Values of •> HEROKU_APP_NAME"
		)
		return
	try:
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		tron = Heroku.app(Config.HEROKU_APP_NAME)
	except BaseException:
		return await m.edit(
			"Please check that you have filled HEROKU_API_KEY\nand your HEROKU_APP_NAME is filled correctly."
		)
	data = tron.get_log()
	if data:
		try:
			file = open("Tron_logs.txt", "w+")
			file.write(data)
			file.close()
			await app.send_document(
				m.chat.id,
				"Tron_logs.txt",
				caption=f"Uploaded By: {mymention}")
			os.remove("Tron_logs.txt")
			await m.delete()
			time.sleep(2)
		except Exception as e:
			await error(m, e)
	else:
		await m.edit(
			"Failed to get logs..."
		)




# get logs from heroku in nekobin link, not as a file 
@app.on_message(gen("textlogs"))
async def logs_text(app, m: Message):
	user = await app.get_me()
	user = user.username
	if not Config.HEROKU_APP_NAME:
		await m.edit(
			"Please fill Values of •> HEROKU_APP_NAME"
		)
		return
	await m.edit(
		"⏳ • hold on..."
	)
	try:
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		tron = Heroku.app(Config.HEROKU_APP_NAME)
	except BaseException:
		return await m.edit(
			"Please check HEROKU_API_KEY and your HEROKU_APP_NAME is filled correctly."
		)
	data = tron.get_log()
	if data:
		try:
			key = (
				requests.post("https://nekobin.com/api/documents", json={"content": data})
				.json()
				.get("result")
				.get("key")
			)
			url = f"https://nekobin.com/{key}"
			text = f"Heroku Logs: [here]({url})"
			await m.edit(text, disable_web_page_preview=True)
		except Exception as e:
			await error(m, e)
	else:
		await m.edit(
			f"Failed to get the logs, try `{PREFIX}logs` cmd..."
		)
