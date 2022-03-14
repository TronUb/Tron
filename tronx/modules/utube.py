from tronx import app, gen

from pytube import YouTube
from pyrogram.types import Message




app.CMD_HELP.update(
	{"utube": (
		"utube",
		{
		"yvinfo [link]" : "Get a youtube video information . . .",
		"yvdl [link]" : "Download any video from YouTube . . ."
		}
		)
	}
)




@app.on_message(gen("yvinfo", allow = ["sudo", "channel"]))
async def videoinfo_handler(_, m: Message):
	reply = m.reply_to_message
	if reply and reply.text:
		link = reply.text
	elif not reply and app.long(m) >= 1:
		link = m.text.split(None, 1)[1]
	elif not reply and app.long(m) == 1:
		return await app.send_edit(m, "Reply to youtube link or give link as a suffix . . .", text_type=["mono"], delme=5)

	await app.send_edit(m, "Getting information . . .", text_type=["mono"])
	yt = YouTube(link)
	thumb_link = yt.thumbnail_url
	data = f"**Title:** {yt.title}\n\n"
	data += f"**Duration:** {app.GetReadableTime(yt.length)}\n\n"
	data += f"**Description:** {yt.description}\n\n"
	data += f"**Views:** {yt.views}\n\n"
	data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

	await app.send_photo(m.chat.id, thumb_link, caption=data)




@app.on_message(gen("yvdl", allow = ["sudo", "channel"]))
async def ytdownload_handler(_, m):
	reply = m.reply_to_message
	await app.send_edit(m, "processing link . . .", text_type=["mono"])
	if not reply:
		if app.long(m) == 1:
			return await app.send_edit(m, "Please reply to a yt link or give me link as a suffix . . .", text_type=["mono"], delme=4)
		elif app.long(m) > 1 and m.command[1].startswith("http://" or "https://") and not m.command[1].isdigit():
			link = m.command[1]
		else:
			return await app.send_edit(m, "Please reply to a link or give me the link as a suffix after command . . .", text_type=["mono"], delme=4)
	elif reply:
		if reply.text and reply.text.startswith("http://" or "https://"):
			link = reply.text
		else:
			return await app.send_edit(m, "Please reply to a link or give me the link as a suffix after command . . .", text_type=["mono"], delme=4)
	else:
		return await app.send_edit(m, "Something went wrong . . .")

	yt = YouTube(link)
	data = yt.streams.all()

	await app.send_edit(m, "**Trying to download **" + f"`{yt.title}`")
	for x in data:
		if x.type == "video" and x.resolution in ("720p" or "1080p") and x.mime_type == "video/mp4":
			try:
				loc = x.download()
				await app.send_video(m.chat.id, loc, caption="**Title:**\n\n" + yt.title)
				await m.delete()
				break
			except Exception as e:
				await error(m, e)

