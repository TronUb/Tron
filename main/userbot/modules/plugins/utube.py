from main import app, gen

from pytube import YouTube
from pytube.exceptions import LiveStreamError

from pyrogram import filters
from pyrogram.handlers import CallbackQueryHandler
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.enums import MessageEntityType, ChatType

from PIL import Image
from pySmartDL import SmartDL




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



def ResizeImage(path: str, size: tuple=(320, 320)):
	img = Image.open(path)
	img.thumbnail(size)
	photo = app.TEMP_DICT+"photo.jpg"
	img.save(photo)
	return photo



def PyDownload(url: str):
	obj = SmartDL(url, app.TEMP_DICT, progress_bar=False)
	obj.start()
	return obj.get_dest()




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
		msg = await app.send_edit("processing link . . .", text_type=["mono"])
		reply = m.reply_to_message
		cmd = m.command
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
		path = PyDownload(yt.thumbnail_url)
		thumbnail = ResizeImage(path)

		try:
			data = yt.streams.filter(mime_type="video/mp4")
		except LiveStreamError:
			await app.send_edit(
				"The owner of this channel is doing live stream, can't download the video.",
				text_type=["mono"],
				delme=3
			)
			return

		if m.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
			if await app.user_exists(m.chat.id, app.bot.id):
				botmsg = await app.bot.send_message(chat_id=m.chat.id, text="`processing link . . .`")

				buttons = []
				temp = []

				for x in range(len(data)):
					name = data[x]

					btn = app.BuildKeyboard(([
						[
							str(name.resolution) + " 🔇" if not name.includes_audio_track else str(name.resolution), 
							str(name.itag)
						]
					]))

					if len(temp) < 3:
						temp.append(btn[0])
					if len(temp) == 3:
						buttons.append(temp)
						temp = []

				await msg.delete()
				await app.bot.send_photo(chat_id=m.chat.id, photo=path, caption=f"**Title:** {yt.title.split('.')[0]}.mp4", reply_markup=InlineKeyboardMarkup(buttons))
				await botmsg.delete()
				app.bot.utubeobject = data

				async def utube_callback(client, cb):
					try:
						if not cb.from_user.id == m.from_user.id:
							await cb.answer("You're not allowed.", show_alert=True)
							return False

						if (int(cb.data) in [int(x.itag) for x in client.utubeobject]):
							botmsg = await client.send_message(cb.message.chat.id, "`Uploading video . . .`")
							obj = client.utubeobject.get_by_itag(int(cb.data))
							if not obj.includes_audio_track:
								await cb.answer("Note: This video doesn't have audio.", show_alert=True)

							loc = obj.download(client.TEMP_DICT)
							await client.send_video(chat_id=cb.message.chat.id, video=loc, caption="**Title:**\n\n" + loc.split("/")[-1], thumb=thumbnail)
							await botmsg.delete()
						else:
							await cb.answer("The message is expired.", show_alert=True)
					except Exception as e:
						print(e)
						await client.error(e)

				app.bot.add_handler(CallbackQueryHandler(callback=utube_callback, filters=filters.regex(r"\d+")))
				return True

		video_found = False
		msg = await app.send_edit("**Trying to download **" + f"`{yt.title}`")
		for x in data:
			if x.type == "video" and x.resolution in ("720p" or "1080p") and x.mime_type == "video/mp4":
				video_found =True
				loc = x.download(app.TEMP_DICT, f"{yt.title.split('.')[0]}.mp4")
				await app.send_video(m.chat.id, loc, caption="**Title:**\n\n" + yt.title, thumb=thumbnail)
				await msg.delete()
				break

		if not video_found:
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
					link = args.text[i.offset : i.length + i.offset] # get link from text
				else:
					link = args.text
			else:
				link = args.text
		else:
			return await app.send_edit("Reply or give args after command.", text_type=["mono"], delme=3)

		yt = YouTube(link)
		try:
			data = yt.streams.filter(only_audio=True)
		except LiveStreamError:
			await app.send_edit(
				"The owner of this channel is doing live stream, can't download the video.",
				text_type=["mono"],
				delme=3
			)
			return

		path = PyDownload(yt.thumbnail_url)
		thumbnail = ResizeImage(path)
		audio_found = False
		msg = await app.send_edit("**Trying to download: **" + f"`{yt.title}`")
		for x in data:
			if x.mime_type == "audio/webm" and x.abr == "160kbps" or x.abr == "128kbps" or x.abr == "70kbps":
				audio_found = True
				loc = x.download(app.TEMP_DICT, f"{yt.title.split('.')[0]}.mp3")
				await app.send_audio(m.chat.id, loc, caption=f"**Title:**\n\n`{yt.title}`", thumb=thumbnail)
				await msg.delete()
				break

		if not audio_found:
			await app.send_edit("I didn't find any good quality audio of this youtube video.", text_type=["mono"], delme=3)  
	except Exception as e:
		await app.error(e)
