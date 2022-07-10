from main import app, gen

from pytube import YouTube
from pyrogram.types import Message
from pyrogram.enums import MessageEntityType




app.CMD_HELP.update(
	{"utube": (
		"utube",
		{
		"ytvinfo [ link | reply ]" : "Get a youtube video information.",
		"ytvdl [ link | reply ]" : "Download any video from YouTube.",
		"ytadl [ link | reply ]" : "Download audios of any video from YouTube."
		}
		)
	}
)




@app.on_message(gen("ytvinfo", allow = ["sudo", "channel"]))
async def ytvideoinfo_handler(_, m: Message):
	try:
		args = app.GetArgs()
		if args:
			if args.text and args.text.entities:
				entity = args.text.entities
				if entity[0].type == MessageEntityType.URL:
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
		data += f"**Description:** {yt.description[:500]}...\n\n"
		data += f"**Views:** {yt.views}\n\n"
		data += f"**Age Restricted:** {'Yes' if yt.age_restricted else 'No'}"

		await app.send_photo(m.chat.id, thumb_link, caption=data)
	except Exception as e:
		await app.error(e)




@app.on_message(gen("ytvdl", allow = ["sudo", "channel"]))
async def ytvideodl_handler(_, m):
	try:
		reply = m.reply_to_message
		cmd = m.command
		msg = await app.send_edit("processing link . . .", text_type=["mono"])
		args = app.GetArgs()
		if args:
			if args.text and args.text.entities:
				entity = args.text.entities
				if entity[0].type == MessageEntityType.URL:
					i = entity[0]
					link = args.text[i.offset:i.length+i.offset] # get link from text
				else:
					link = args.text
			else:
				link = args.text
		else:
			return await app.send_edit("Reply or give args after command.", text_type=["mono"], delme=3)

		yt = YouTube(link)
		data = yt.streams.all()
		video_found = False
		msg = await app.send_edit("**Trying to download **" + f"`{yt.title}`")
		for x in data:
			if x.type == "video" and x.resolution in ("720p" or "1080p") and x.mime_type == "video/mp4":
				video_found =True
				loc = x.download()
				await app.send_video(m.chat.id, loc, caption="**Title:**\n\n" + yt.title)
				await msg.delete()
				break

		if not found_video:
			await app.send_edit("I didn't found any good quality video of this YouTube link", text_type=["mono"], delme=3)   
	except Exception as e:
		await app.error(e)




@app.on_message(gen("ytadl", allow = ["sudo", "channel"]))
async def ytvideodl_handler(_, m):
	try:
		reply = m.reply_to_message
		cmd = m.command
		msg = await app.send_edit("processing link . . .", text_type=["mono"])
		args = app.GetArgs()
		if args:
			if args.text and args.text.entities:
				entity = args.text.entities
				if entity[0].type == MessageEntityType.URL:
					i = entity[0]
					link = args.text[i.offset:i.length+i.offset] # get link from text
				else:
					link = args.text
			else:
				link = args.text
		else:
			return await app.send_edit("Reply or give args after command.", text_type=["mono"], delme=3)

		yt = YouTube(link)
		data = yt.streams.filter(only_audio=True)
		found_audio = False
		msg = await app.send_edit("**Trying to download: **" + f"`{yt.title}`")
		for x in data:
			if x.mime_type == "audio/webm" and x.abr == "160kbps" or x.abr == "128kbps" or x.abr == "70kbps":
				found_audio = True
				loc = x.download()
				await app.send_audio(m.chat.id, loc, caption=f"**Title:**\n\n`{yt.title}`")
				await msg.delete()
				break

		if not found_audio:
			await app.send_edit("I didn't find any good quality audio of this youtube video.", text_type=["mono"], delme=3)  
	except Exception as e:
		await app.error(e)

