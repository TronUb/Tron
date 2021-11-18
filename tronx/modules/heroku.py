import os
import sys
import math
import requests
import heroku3
import json

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
	send_edit,
	long,
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
async def turn_off_dyno(_, m: Message):
	await not_heroku(m)
	if Config.LOG_CHAT:
		await app.send_message(
			Config.LOG_CHAT, 
			"#shutdown \n" 
			"Bot is now turned off !!\nTurn it on manually on heroku.com"
			)
	else:
		pass
	Heroku = heroku3.from_key(Config.HEROKU_API_KEY).apps()[Config.HEROKU_APP_NAME]
	if Heroku:
		Heroku.process_formation()["worker"].scale(0)
		await send_edit(
			m, 
			"Dynos are truned off, if you want turn them on manually from heroku.com",
			mono=True
		)
	else:
		sys.exit(0)




# restart your bot 
@app.on_message(gen("restart"))
async def restart_app(_, m: Message):
	await not_heroku(m)
	try:
		await send_edit(m, "Restarting . . .", mono=True)
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.apps()[Config.HEROKU_APP_NAME]
		restart = heroku_app.restart()
		if restart:
			return await send_edit(
				m, 
				"Restarted . . .!\nPlease wait for 3 min or more to restart userbot . . .", 
				mono=True
			)
		else:
			return await send_edit(
				m, 
				"Failed to restart userbot, try again later . . .",
				mono=True
			)
	except Exception as e:
		await error(m, e)




# get usage of your dyno hours from heroku
@app.on_message(gen("usage"))
async def dynostats(_, m: Message):
	await not_heroku(m)

	Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
	await send_edit(m, "Checking usage . . .", mono=True)
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
				return await send_edit(
					msg, 
					"Error: something bad happened`\n\n" f"> {r.reason}\n",
					mono=True
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

			await send_edit(
				msg, 
				"**Dyno Usage**:\n\n"
				f"**Total Dyno Hours:** `550 Hours`\n\n"
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
async def heroku_vars(_, m: Message):
	await not_heroku(m)
	try:
		await send_edit(
			m, 
			"Fetching all vars from Heroku . . .", 
			mono=True
			)
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.apps()[Config.HEROKU_APP_NAME]
		heroku_vars = zen.config()
		vars_dict = heroku_vars.to_dict()
		vars_keys = list(vars_dict.keys())
		msg = "**Here are vars setup for Tronuserbot**\n\n"
		num = 0
		for i in vars_keys:
			num += 1
			msg += f"**{num}**: `{i}`\n"

		msg += f"\n**Total `{num}` vars found.**"
		return await send_edit(
			m, 
			msg
		)
	except Exception as e:
		await error(m, e)




# set vars in heroku 
@app.on_message(gen("setvar"))
async def setvar(_, m: Message):
	await not_heroku(m)

	Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
	zen = Heroku.app(Config.HEROKU_APP_NAME)

	if long(m) < 3:
		return await send_edit(
			m, 
			f"`{PREFIX}setvar [key] [value]`"
		)
	elif long(m) >= 3:
		key = m.command[1]
		value = m.command[2]
		heroku_vars = zen.config()
		try:
			if key and value in heroku_vars:
				await send_edit(
					m, 
					f"{key} is already in vars with value {value}"
				)
			elif not key in heroku_vars:
				await send_edit(
					m, 
					f"Added var •> `{key}` = `{value}`", 
					disable_web_page_preview=True
				)
				heroku_vars[key] = value
			else:
				await send_edit(
					m,
					"Something went wrong, try again later !",
					mono=True
				)
		except Exception as e:
			await error(m, e)




# get vars from heroku vars
@app.on_message(gen("getvar"))
async def getvar(_, m: Message):
	await not_heroku(m)
	if long(m) == 1:
		return await send_edit(
			m, 
			f"`{PREFIX}getvar [key name]`"
		)
	elif long(m) >= 2:
		key = m.command[1]
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.apps()[Config.HEROKU_APP_NAME]
		heroku_vars = zen.config()
		try:
			if heroku_vars:
				await send_edit(
					m, 
					f"**Key exists:**\n\n`{key}` = `{heroku_vars[key]}`"
				)
			else:
				await send_edit(
					m, 
					"Failed to get heroku key . . .",
					mono=True
				)
		except Exception as e:
			await error(m, e)




# delete vars in heroku 
@app.on_message(gen("delvar"))
async def delvar(_, m: Message):
	await not_heroku(m)
	elif long(m) == 1:
		return await send_edit(
			m, 
			f"{PREFIX}delvar [key name]", 
			mono=True
		)
	elif long(m) >= 2:
		await send_edit(
			m, 
			"Verifying var in heroku config vars . . .", 
			delme=3, 
			mono=True
		)

		key = m.command[1]
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.apps()[Config.HEROKU_APP_NAME]
		heroku_vars = zen.config()

		if key not in heroku_vars:
			return await send_edit(
				m, 
				f"**`{key}`** does not exist in heroku vars . . .", 
				delme=3
			)
		try:
			del heroku_vars[key]
		except Exception as e:
			return await error(app, m, e)
		await send_edit(
			m, 
			f"**`{key}`** Deleted Successfully from heroku vars . . . !", 
			delme=3
		)
	else:
		await send_edit(
			m, 
			"Usage: `{PREFIX}delvar [key name]` use this format . . .",
			delme=3
		)




# get logs from heroku in file format (.txt)
@app.on_message(gen("logs"))
async def logs(_, m: Message):
	await not_heroku(m)
	await send_edit(
		m, 
		"⏳ • hold on . . .", 
		mono=True
		)
	try:
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.app(Config.HEROKU_APP_NAME)
	except BaseException:
		return await send_edit(
			m, 
			"Please try again later !", 
			delme=3,
			mono=True
		)
	data = zen.get_log()
	if data:
		try:
			file = open("Tron_logs.txt", "w+")
			file.write(data)
			file.close()
			await app.send_document(
				m.chat.id,
				f"{USER_NAME}_logs.txt",
				caption=f"Uploaded By: {mymention()}")
			os.remove(f"{USER_NAME}_logs.txt")
			await m.delete()
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			"Failed to get logs . . .",
			delme=3
		)




# get logs from heroku in nekobin link, not as a file 
@app.on_message(gen(["textlogs", "tlogs"]))
async def logs_in_text(_, m: Message):
	await not_heroku(m)
	await send_edit(
		m, 
		"⏳ • hold on . . . ", mono=True
	)
	try:
		Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
		zen = Heroku.app(Config.HEROKU_APP_NAME)
	except BaseException:
		return await send_edit(
			m, 
			"Please try again later !", 
			delme=3,
			mono=True
		)
	data = zen.get_log()
	if data:
		try:
			key = (requests.post("https://nekobin.com/api/documents", json={"content":data}).json().get("result").get("key"))
			url = f"https://nekobin.com/{key}"
			text = f"Heroku Logs: [here]({url})"
			await send_edit(m, text, disable_web_page_preview=True)
		except Exception as e:
			await error(m, e)
	else:
		await send_edit(
			m, 
			f"Failed to get the logs, try `{PREFIX}logs` cmd . . .",
			delme=3
		)




async def not_heroku(m: Message):
	if not (
		Config.HEROKU_APP_NAME
		and Config.HEROKU_API_KEY
		):
		return await send_edit(
			m, 
			"Please fill heroku credentials for this command to work [`HEROKU_APP_NAME`, `HEROKU_API_KEY`"
		)
	else:
		pass
