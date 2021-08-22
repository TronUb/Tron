import pytz, datetime, time
from asyncio import sleep

from pyrogram.types import Message

from tronx import (
	app,
	log,
)

from config import Config



# date
def showdate():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_date = datetime.datetime.now(today)
	mydate = get_date.strftime("%d %b %Y")
	return mydate


# time
def showtime():
	today = pytz.timezone(
		Config.TIME_ZONE
		)
	get_time = datetime.datetime.now(today)
	mytime = get_time.strftime("%r")
	return mytime


# send or edit msg
async def send_edit(
	m: Message, 
	text, 
	parse_mode="markdown", 
	disable_web_page_preview=False
	):
	try:
		await m.edit(text)
	except:
		await app.send_message(
			m.chat.id,
			text
			)


# send msg
async def sendmsg(m: Message, text):
	try:
		await app.send_message(
			m.chat.id,
			text
			)
	except Exception as e:
		await error(m, e)
	return


# show error
async def error(m: Message, e):
	teks = f"Traceback Report:\n\n"
	teks += f"Date: {showdate()}\nTime: {showtime()}\n\n"
	teks += f"This can be a error in tronuserbot, if you want you can forward this to @tronuserbot.\n\n" 
	teks += f"Command: {m.text}\n\n"
	teks += f"Error:\n\n"
	teks += f"{e}"
	try:
		await app.send_message(
			Config.LOG_CHAT,
			teks
			)
	except:
		print(teks)
	log.error("Please check your log chat for traceback error !")
	return 


# delete msg
async def delete(m: Message, sec: int = 0):
	if not sec > 600: # 10 min
		sleep(sec)
		await m.delete()
	else:
		log.error("maximum sleep of 10 ( 600 sec ) minutes")
	return
