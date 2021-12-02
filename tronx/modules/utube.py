from tronx import (
	app,
)

from pytube import YouTube
from pyrogram.types import Message
from tronx.helpers import (
	get_readable_time,
	long,
	gen,
	send_edit,
)




CMD_HELP.update(
	{"utube": (
		"utube",
		{
		"vinfo" : "Get a youtube video information . . ."
		}
		)
	}
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

	await send_edit(m, "Getting information . . .", mono=True)
	yt = YouTube(link)
	thumb_link = yt.thumbnail_url
	data = f"**Title:** {yt.title}\n\n"
	data += f"**Duration:** {get_readable_time(yt.length)}\n\n"
	data += f"**Description:** {yt.description}\n\n"
	data += f"**Views:** {yt.views}\n\n"
	data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

	await app.send_photo(m.chat.id, thumb_link, caption=data)
