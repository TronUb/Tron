import random
import asyncio

from datetime import datetime

from pyrogram.types import Message

from tronx import app, gen




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




@app.on_message(gen(["ping", "pong"], allow = ["sudo", "channel"]))
async def ping_handler(_, m: Message):
	try:

		if app.long(m) == 1:
			start = datetime.now()
			m = await app.send_edit(m, ". . .", text_type=["mono"])
			end = datetime.now()
			m_s = (end - start).microseconds / 1000
			await app.send_edit(
				m, 
				f"**Pöng !**\n`{m_s} ms`\n⧑ {app.UserMention()}", 
				disable_web_page_preview=True
			)
		elif app.long(m) == 2:
			cmd = m.command
			count = int(cmd[1]) if cmd[1] and cmd[1].isdigit() else 0
			if count <= 1:
				return await app.send_edit(m, f"Use `{app.UserPrefix().split()[0]}ping` for pings less than 1.", delme=4)

			else:
				try:
					num = int(count) + 1
					for x in range(1, num):
						m = await infinite(m)
						await app.send_edit(m, ". . .", text_type=["mono"])
						await asyncio.sleep(0.30)
					await app.send_edit(m, "".join(pings))
				except Exception as e:
					await app.error(m, e)
		else:
			return await app.send_edit(m, "Something went wrong in ping module.", delme=2)
	except Exception as e:
		await app.error(m, e)




# function to create lots of pings
async def infinite(m: Message):
	start = datetime.now()
	m = await app.send_edit(m, random.choice(data)) # MessageNotModified 
	end = datetime.now()
	m_s = (end - start).microseconds / 1000
	msg = f"Pöng !\n{m_s} ms\n⧑ {app.UserMention()}\n\n"
	pings.append(msg)
	return m


