import re
import os
import time
import json
import math
import asyncio
import traceback

from io import BytesIO

from pySmartDL import SmartDL
from datetime import datetime

from pyrogram import filters, errors
from pyrogram.types import Message

from tronx import app

from tronx.helpers import (
	gen,
)




app.CMD_HELP.update(
	{"download" : (
		"download",
		{
		"ls" : "Find file location in the local directories.",
		"download [Reply to media]" : "Downloads media files in local server.",
		"dl [reply to file]" : "Downloads media files in local server.",
		"upload [path]" : "Upload files from local server to telegram",
		"ul [path]" : "Upload files from local server to telegram.",
		"batchup [path]" : "Upload batch files from a local directories."
		}
		)
	}
)




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.on_message(gen("ls", allow =["sudo"]))
async def list_directories(_, m: Message):
	location = "." if app.long(m) == 1 else m.command[1] if app.long(m) >= 2 else None

	location = os.path.abspath(location)
	if not location.endswith("/"):
		location += "/"
	OUTPUT = f"Files in `{location}`:\n\n"

	m = await app.send_edit(m, "Fetching files . . .", mono=True)

	try:
		files = os.listdir(location)
		files.sort()  # Sort the files
	except FileNotFoundError:
		return await app.send_edit(m, f"No such file or directory {location}", delme=2)

	collect = []
	collect.clear()

	for file in files:
		if not file.endswith(".session") and not file in ["__pycache__", ".git", ".github", ".profile.d", ".heroku", ".cache"]:
			if os.path.isfile(f"{location}/{file}"):
				collect.append(f"📑 `{file}` ({app.DictSize(os.path.abspath(location+file))})")
			if os.path.isdir(f"{location}/{file}"):
				collect.append(f"🗂️ `{file}` ({app.DictSize(os.path.abspath(location+file))})")
					
	collect.sort() # sort the files
	file = "\n".join(collect)
	OUTPUT += f"{file}"

	if len(OUTPUT) > 4096:
		await m.delete()
		await app.create_file(
				m, 
				app, 
				filename="dict.txt", 
				text=OUTPUT
			)
	elif OUTPUT.endswith("\n\n"):
		return await app.send_edit(m, f"No files in `{location}`", delme=4)
	elif len(OUTPUT) <= 4096:
		await app.send_edit(m, OUTPUT)





@app.on_message(gen(["download", "dl"], allow =["sudo"]))
async def download_media(_, m: Message):
	reply = m.reply_to_message
	if reply and reply.media:
		try:
			start_t = datetime.now()
			c_time = time.time()

			m = await app.send_edit(m, "• Downloading . . .", mono=True)
			location = await app.download_media(
				message=reply,
				progress=app.ProgressForPyrogram,
				progress_args=("Downloading file . . .", m, c_time),
			)

			end_t = datetime.now()
			duration = app.GetReadableTime((end_t - start_t).seconds)

			if location is None:
				await app.send_edit(m, "Download failed, please try again.", mono=True)
			else:
				await app.send_edit(m, f"**Downloaded to •>**\n\n```{location}```\n\n**Time:** `{duration}`",)
		except Exception as e:
			await app.error(m, e)
			await app.send_edit(m, f"Failed To Download, look in log chat for more info.")

	elif app.long(m) > 1:
		try:
			start_t = datetime.now()
			the_url_parts = " ".join(m.command[1:])
			url = the_url_parts.strip()
			custom_file_name = os.path.basename(url)
			if "|" in the_url_parts:
				url, custom_file_name = the_url_parts.split("|")
				url = url.strip()
				custom_file_name = custom_file_name.strip()
			download_file_path = os.path.join(app.TEMP_DICT, custom_file_name)
			downloader = SmartDL(url, download_file_path, progress_bar=False)
			downloader.start(blocking=False)
			c_time = time.time()
			while not downloader.isFinished():
				total_length = downloader.filesize if downloader.filesize else None
				downloaded = downloader.get_dl_size()
				display_message = ""
				now = time.time()
				diff = now - c_time
				percentage = downloader.get_progress() * 100
				speed = downloader.get_speed(human=True)
				elapsed_time = round(diff) * 1000
				progress_str = "**[{0}{1}]**\n**Progress:** __{2}%__".format(
					"".join(["●" for i in range(math.floor(percentage / 5))]),
					"".join(["○" for i in range(20 - math.floor(percentage / 5))]),
					round(percentage, 2),
				)
				estimated_total_time = downloader.get_eta(human=True)
				try:
					current_message = f"__**Trying to download...**__\n"
					current_message += f"**URL:** `{url}`\n"
					current_message += f"**File Name:** `{custom_file_name}`\n"
					current_message += f"{progress_str}\n"
					current_message += (
						f"__{app.HumanBytes(downloaded)} of {app.HumanBytes(total_length)}__\n"
					)
					current_message += f"**Speed:** __{speed}__\n"
					current_message += f"**ETA:** __{estimated_total_time}__"
					if round(diff % 10.00) == 0 and current_message != display_message:
						await app.send_edit(
							m,
							disable_web_page_preview=True, 
							text=current_message
						)
						display_message = current_message
						await asyncio.sleep(2)
				except errors.MessageNotModified: 
					pass
				except Exception as e:
					app.log.info(str(e))
					pass
			m = await app.send_edit(m, "• Downloading . . .", mono=True)
			if os.path.exists(download_file_path):
				end_t = datetime.now()
				ms = (end_t - start_t).seconds
				await app.send_edit(
					m,
					f"**Downloaded to:** `{download_file_path}`\n**Time Taken:** `{ms}` seconds.\nDownload Speed: {round((total_length/ms), 2)}",
				)
		except Exception:
			exc = traceback.format_exc()
			return await app.send_edit(
				m, 
				f"Failed Download!\n\n{exc}"
				)
	else:
		await app.send_edit(m, "Reply to a Telegram Media to download it to local server.", mono=True, delme=2)





@app.on_message(gen(["upload", "ul"], allow =["sudo"]))
async def upload_as_document(_, m: Message):
	if app.long(m) > 1:
		local_file_name = m.text.split(None, 1)[1]
		if os.path.exists(local_file_name):
			m = await app.send_edit(m, "Uploading . . .", mono=True)
			start_t = datetime.now()
			c_time = time.time()
			doc_caption = os.path.basename(local_file_name)
			await app.send_edit(m, f"Uploading `{doc_caption}` . . .")

			await m.reply_document(
				document=local_file_name,
				caption=doc_caption,
				disable_notification=True,
				reply_to_message_id=m.message_id,
				progress=app.ProgressForPyrogram,
				progress_args=("Uploading file . . .", m, c_time),
			)

			end_t = datetime.now()
			ms = (end_t - start_t).seconds
			await app.send_edit(m, f"Uploaded in `{ms}` seconds.", delme=2)
		else:
			await app.send_edit(m, "404: directory not found . . .",mono=True, delme=5)
	else:
		await app.send_edit(m, f"`{app.PREFIX}upload [file path ]` to upload to current Telegram chat", delme=4)





@app.on_message(gen(["batchup", "bcp"], allow =["sudo"]))
async def batch_upload(_, m: Message):
	if app.long(m) == 1:
		return await app.send_edit(m, "Give me a location to upload files from the directory . . .", delme=2, mono=True)

	elif app.long(m) > 1:
		temp_dir = m.command[1]
		if not temp_dir.endswith("/"):
			temp_dir += "/"

	if os.path.exists(temp_dir):
		try:
			m = await app.send_edit(m, f"Uploading Files from `{temp_dir}` . . .")
			files = os.listdir(temp_dir)
			files.sort()
			for file in files:
				if file.endswith(".py"):
					c_time = time.time()
					required_file_name = temp_dir + file
					thumb_image_path = await IsThumbExists(required_file_name)
					doc_caption = os.path.basename(required_file_name)
					log.info(f"Uploading {required_file_name} from {temp_dir} to Telegram.")

					await app.send_document(
						chat_id=m.chat.id,
						document=required_file_name,
						thumb=thumb_image_path,
						caption=doc_caption,
						disable_notification=True,
					)
					await app.send_edit(m, f"Uploaded all files from Directory `{temp_dir}`", delme=3)
					app.log.info("Uploaded all files in batch !!")

		except Exception as e:
			await app.error(m, e)
	else:
		return await app.send_edit(m, "404: directory not found . . .", delme=2)

