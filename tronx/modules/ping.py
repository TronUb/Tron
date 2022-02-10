import os
import time
import random
import asyncio

from sys import platform
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message, User

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"ping" : (
		"ping",
		{
		"ping" : "Shows you the response speed of the bot.",
		"ping [ number ]" : "Make infinite pings, don't overuse."
		}
		)
	}
)




# animations
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

pings = []
pings.clear()




@app.on_message(gen(["ping", "pong"], allow_channel=True))
async def pingme(_, m: Message):
	if app.long(m) == 1:
		start = datetime.now()
		m = await app.send_edit(m, ". . .", mono=True)
		end = datetime.now()
		m_s = (end - start).microseconds / 1000
		await app.send_edit(
			m, 
			f"**Pöng !**\n`{m_s} ms`\n⧑ {app.UserMention()}", 
			disable_web_page_preview=True
			)
	elif app.long(m) == 2:
		count = m.command[1]
		text = int(m.command[1])
		if text == 1:
			return await app.send_edit(m, "If you need one ping use only `.ping`", delme=2)

		elif text == 0:
			return await app.send_edit(m, "try a greater number like 2.", delme=2, mono=True)

		else:
			try:
				num = int(count) + 1
				for x in range(1, num):
					m = await infinite(m)
					await app.send_edit(m, ". . .", mono=True)
					time.sleep(0.50)
				await app.send_edit(m, "".join(pings))
			except Exception as e:
				await app.error(m, e)
	else:
		return await app.send_edit(m, "Something went wrong in ping module.", delme=2)




# function to create lots of pings
async def infinite(m: Message):
	start = datetime.now()
	m = await app.send_edit(m, random.choice(data))
	end = datetime.now()
	ms = (end - start).microseconds / 1000
	msg = f"Pöng !\n{ms} ms\n⧑ {app.UserMention()}\n\n"
	pings.append(msg)
	return m


