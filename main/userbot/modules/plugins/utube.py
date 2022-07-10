from main import app, gen

from pytube import YouTube
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType




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
async def ytvideoinfo_handler(_, m: Message):
	try:
		args = app.GetArgs()
		if args:
			if args.text and args.text.entities:
				entity = args.text.entities
				if isinstance(entity[0].type,  MessageEntityType.URL):
					i = entity[0]
					link = args.text[i.offset:i.length+i.offset] # get link from text
				else:
					link = args.text
			else:
				link = args.text
		else:
			return await app.send_edit("Reply or give args after command.", text_type=["mono"], delme=3)

		await app.send_edit("Getting information . . .", text_type=["mono"])
		yt = YouTube(link)
		thumb_link = yt.thumbnail_url
		data = f"**Title:** {yt.title}\n\n"
		data += f"**Duration:** {app.GetReadableTime(yt.length)}\n\n"
		data += f"**Description:** {yt.description}\n\n"
		data += f"**Views:** {yt.views}\n\n"
		data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

		await app.send_photo(m.chat.id, thumb_link, caption=data)
	except Exception as e:
		await app.error(e)




@app.on_message(gen("yvdl", allow = ["sudo", "channel"]))
async def ytvideodl_handler(_, m):
	reply = m.reply_to_message
	cmd = m.command
	await app.send_edit("processing link . . .", text_type=["mono"])
	if not reply:
		if app.long() == 1:
			return await app.send_edit("Please reply to a yt link or give me link as a suffix . . .", text_type=["mono"], delme=4)
		elif app.long() > 1 and cmd[1]:
			link = cmd[1]
		else:
			return await app.send_edit("Please reply to a link or give me the link as a suffix after command . . .", text_type=["mono"], delme=4)
	elif reply:
		if reply.text and reply.entities:
			entity = reply.entities[0]
			if isinstance(entity, MessageEntityType.URL):
				link = reply.text[entity.offset:entity.length+entity.offsef]
			else:
				link = reply.text

		else:
			return await app.send_edit("Please reply to a link or give me the link as a suffix after command . . .", text_type=["mono"], delme=4)
	else:
		return await app.send_edit("Something went wrong . . .")

	yt = YouTube(link)
	data = yt.streams.all()

	await app.send_edit("**Trying to download **" + f"`{yt.title}`")
	for x in data:
		if x.type == "video" and x.resolution in ("720p" or "1080p") and x.mime_type == "video/mp4":
			try:
				loc = x.download()
				await app.send_video(m.chat.id, loc, caption="**Title:**\n\n" + yt.title)
				await m.delete()
				break
			except Exception as e:
				await app.error(e)

