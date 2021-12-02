from tronx import (
	app,
	gen,
)

from pytube import YouTube
from pyrogram.types import Message
from tronx.helpers import (
	get_readable_time,
	long,
)




@app.on_message(gen("vinfo"))
async def utube_info(_, m: Message):
	reply = m.reply_to_message
	if reply and reply.text:
		link = reply.text
	elif not reply and long(m) >= 1:
		link = m.text.split(None, 1)[1]
	elif not reply and long(m) == 1:
		return await send_edit(m, "Reply to youtube link or give link as a suffix . . .", mono=True, delme=5)

	yt = YouTube(link)
	thumb_link = yt.thumbnail_url
	data = f"**Title:** {yt.title}\n"
	data += f"**Duration:** {get_readable_time(yt.length)}\n"
	data += f"**Description:** {yt.description}\n"
	data += f"**Views:** {yt.views}\n"
	data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

	await app.send_photo(m.chat.id, thumb_link, caption=data)
