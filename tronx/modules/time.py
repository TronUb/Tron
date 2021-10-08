import pytz
import time
import datetime

from pyrogram import filters
from pyrogram.types import Message

from tronx import (
	app, 
	CMD_HELP,
	Config,
	PREFIX
	)

from tronx.helpers import (
	gen,
	error,
	send_edit,
	#others
	showtime,
	showdate,
)




CMD_HELP.update( 
	{"time" : (
		"time",
		{
		"today" : "Get date & time information, set your `TIME_ZONE` to get correct time & date.", 
		"time" : "Get time information of your city.",
		"date" : "Get date information of your city."
		}
		)
	}
)




@app.on_message(gen("today"))
async def today(_, m: Message):
	weekday = datetime.datetime.today().weekday()
	if weekday == 0:
		today = "Monday"
	elif weekday == 1:
		today = "Tuesday"
	elif weekday == 2:
		today = "Wednesday"
	elif weekday == 3:
		today = "Thursday"
	elif weekday == 4:
		today = "Friday"
	elif weekday == 5:
		today = "Saturday"
	elif weekday == 6:
		today = "Sunday"
	my_time = pytz.timezone(Config.TIME_ZONE)
	
	time = datetime.datetime.now(my_time)

	text = f"Today is `{today}`, "
	text += f"{time.strftime('%d %b %Y')}\n" 
	text += f"Time: {time.strftime('%r')}"
	await send_edit(
		m,
		text
		)




@app.on_message(gen("time"))
async def what(_, m: Message):
	await send_edit(m, f"Today's time: `{showtime()}`")




@app.on_message(gen("date"))
async def what(_, m: Message):
	await send_edit(m, f"Today's date: `{showdate()}`")
