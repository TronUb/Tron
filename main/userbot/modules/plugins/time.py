""" time plugin """

import datetime
import pytz

from pyrogram.types import Message

from main import app, gen




app.CMD_HELP.update(
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
async def today_handler(_, m: Message):
    """ today handler for time plugin """
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
    my_time = pytz.timezone(app.TIME_ZONE)

    time = datetime.datetime.now(my_time)

    text = f"Today is `{today}`, "
    text += f"{time.strftime('%d %b %Y')}\n"
    text += f"Time: {time.strftime('%r')}"
    await app.send_edit(text)




@app.on_message(gen("time"))
async def time_handler(_, m: Message):
    """ time handler for time plugin """
    await app.send_edit(f"Today's time: `{app.showtime()}`")




@app.on_message(gen("date"))
async def date_handler(_, m: Message):
    """ date handler for time plugin """
    await app.send_edit(f"Today's date: `{app.showdate()}`")
