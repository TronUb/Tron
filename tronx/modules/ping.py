import os
import time
import random
import asyncio

from sys import platform
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message, User

from tronx import (
	app, 
	CMD_HELP, 
	StartTime, 
	USER_NAME, 
	USER_ID,
	Config,
	PREFIX
	)

from tronx.helpers import (
	error,
	gen,
	send_edit,
	# others 
	mention_markdown,
)

from . import SUDO_USERS




pings = []


CMD_HELP.update(
	{"ping" : (
		"ping",
		{
		"ping" : "Shows you the response speed of the bot."
		}
		)
	}
)

# custom name first, or real tg name
if USER_NAME:
    name = USER_NAME
else:
    name = Config.USER_NAME


# To avoid message not modified error 
# you will still get floodwait error 
# if tried a greater number
data = [ 
	"🕜", 
	"🕡", 
	"🕦", 
	"🕣", 
	"🕥", 
	"🕧", 
	"🕓", 
	"🕔", 
	"🕒", 
	"🕑", 
	"🕐"
]


@app.on_message(gen("ping"))
async def pingme(_, m: Message):
	if len(m.command) == 1:
		start = datetime.now()
		await send_edit(
			m,
			"`...`"
			)
		end = datetime.now()
		m_s = (end - start).microseconds / 1000
		await send_edit(
			m, 
			f"**Pöng !**\n`{m_s} ms`\n⧑ {mention_markdown(USER_ID, name)}", 
			disable_web_page_preview=True
			)
	elif len(m.command) == 2:
		count = m.command[1]
		text = int(m.command[1])
		if text == 1:
			await send_edit(
				m, 
				"If you need one ping use only `.ping`"
				)
			return
		elif text == 0:
			await send_edit(
				m, 
				"try a greater number like 2."
				)
			return
		else:
			try:
				num = int(count) + 1
				for x in range(1, num):
					await infinite(m)
					await send_edit(
						m, 
						"..."
						)
					time.sleep(0.50)
				await send_edit(
					m, 
					"".join(pings)
					)
				pings.clear()
			except Exception as e:
				await error(m, e)
	else:
		await send_edit(
			m, 
			"Something went wrong in ping module."
			)
		return




# function to create pings
async def infinite(m:Message):
	start = datetime.now()
	mid = await send_edit(
		m, 
		random.choice(data)
		)
	end = datetime.now()
	ms = (end - start).microseconds / 1000
	msg = f"Pöng !\n{ms} ms\n⧑ {mention_markdown(USER_ID, name)}\n\n"
	pings.append(msg)


